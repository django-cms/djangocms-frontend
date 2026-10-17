import { watch } from 'node:fs';
import { mkdir, readdir, writeFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
import autoprefixer from 'autoprefixer';
import CleanCSS from 'clean-css';
import postcss from 'postcss';
import * as sass from 'sass';

const root = fileURLToPath(new URL('../', import.meta.url));
const source = path.join(root, 'private/sass');
const destination = path.join(root, 'djangocms_frontend/static/djangocms_frontend/css');
const debug = process.argv.includes('--debug');
const header = '/*\n    This file is generated.\n    Do not edit directly.\n' +
    '    Edit original files in\n    /private/sass instead\n */ \n\n';

async function build() {
    await mkdir(destination, { recursive: true });
    const entries = (await readdir(source)).filter(
        name => !name.startsWith('_') && /\.(scss|sass)$/.test(name),
    ).sort();

    for (const entry of entries) {
        const output = path.join(destination, entry.replace(/\.(scss|sass)$/, '.css'));
        const compiled = sass.compile(path.join(source, entry), {
            sourceMap: debug,
            sourceMapIncludeSources: debug,
        });
        const prefixed = await postcss([
            autoprefixer({ cascade: false }),
            {
                postcssPlugin: 'generated-file-header',
                Once(css) {
                    css.prepend(postcss.parse(header).nodes);
                },
            },
        ]).process(
            compiled.css,
            {
                from: path.join(source, entry),
                to: output,
                map: debug ? {
                    prev: compiled.sourceMap,
                    inline: false,
                    annotation: true,
                    sourcesContent: true,
                } : false,
            },
        );
        for (const warning of prefixed.warnings()) {
            console.warn(warning.toString());
        }

        let css = prefixed.css;
        if (!debug) {
            const minified = new CleanCSS({ rebase: false }).minify(css);
            if (minified.errors.length) {
                throw new Error(minified.errors.join('\n'));
            }
            for (const warning of minified.warnings) {
                console.warn(warning);
            }
            css = header + minified.styles;
        }
        if (prefixed.map) {
            await writeFile(output + '.map', prefixed.map.toString());
        }
        await writeFile(output, css);
        console.log(`Built ${path.relative(root, output)}`);
    }
}

if (process.argv.includes('--watch')) {
    let pending = Promise.resolve();
    let timer;
    const rebuild = () => {
        pending = pending.then(build).catch(error => console.error(error));
    };
    watch(source, { recursive: true }, (event, filename) => {
        if (filename && !/\.(scss|sass)$/.test(filename)) return;
        clearTimeout(timer);
        timer = setTimeout(rebuild, 100);
    });
    rebuild();
    console.log('Watching private/sass for changes…');
} else {
    await build();
}
