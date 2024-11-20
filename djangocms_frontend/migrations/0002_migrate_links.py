from django.db import migrations


def convert_item(config, direction):
    """Convert FrontendUIItem config to new djangocms_link format."""
    if direction == "forward":
        if config.get("external_link"):
            if (config.get("anchor") or "").strip():
                anchor = "#" + config.get("anchor").strip()
                del config["anchor"]
            else:
                anchor = ""
            config["link"] = {"external_link": config.get("external_link") + anchor}
            del config["external_link"]
            return True
        if config.get("internal_link"):
            model = config.get("internal_link").get("model")
            pk = config.get("internal_link").get("pk")
            config["link"] = {"internal_link": f"{model}:{pk}"}
            if config.get("anchor"):
                config["link"]["anchor"] = "#" + config.get("anchor")
                del config["anchor"]
            del config["internal_link"]
            return True
        if config.get("file_link"):
            config["link"] = {"file_link": config.get("file_link").get("pk")}
            del config["file_link"]
            return True
        if config.get("phone"):
            config["link"] = {"external_link": f"tel:{config.get('phone')}"}
            del config["phone"]
            return True
        if config.get("mailto"):
            config["link"] = {"external_link": f"mailto:{config.get('mailto')}"}
            del config["mailto"]
            return True
        if config.get("anchor"):
            config["link"] = {"external_link": "#" + config.get('anchor')}
            del config["anchor"]
            return True

    elif direction == "backward" and config.get("link"):
        link = config.get("link")
        if link.get("external_link"):
            if "#" in link.get("external_link"):
                config["anchor"] = link.get("external_link").split("#", 1)[1]
            ext = link.get("external_link").split("#", 1)[0]
            if ext.startswith("tel:"):
                config["phone"] = ext[4:]
            elif ext.startswith("mailto:"):
                config["mailto"] = ext[7:]
            elif ext:
                config["external_link"] = ext
        elif link.get("internal_link"):
            model, pk = link.get("internal_link").split(":")
            config["internal_link"] = {"model": model, "pk": int(pk)}
            if link.get("anchor"):
                config["anchor"] = link.get("anchor")[1:]
        elif link.get("file_link"):
            config["file_link"] = {"model": "filer.file", "pk": int(link.get("file_link"))}
        del config["link"]
        return True
    return False


def convert(apps, schema_editor, direction):
    FrontendUIItem = apps.get_model("djangocms_frontend", "FrontendUIItem")
    for item in FrontendUIItem.objects.all():
        changed = convert_item(item.config, direction)
        if changed:
            item.save()


class Migration(migrations.Migration):
    dependencies = [
        ("djangocms_frontend", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(
            lambda apps, schema_editor: convert(apps, schema_editor, "forward"),
            lambda apps, schema_editor: convert(apps, schema_editor, "backward"),
            elidable=True
        ),
    ]
