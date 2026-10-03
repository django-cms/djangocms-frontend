from collections.abc import Mapping
from typing import Any

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from djangocms_picture.backends import PictureReference, StoredPictureSource, get_backends
from djangocms_picture.fields import BackendImageField, BackendSelection


def get_picture_reference(
    config: Mapping[str, Any],
    field_name: str,
    *,
    external_field_name: str | None = None,
) -> PictureReference | None:
    """Read current references and legacy frontend filer/URL values."""

    if external_field_name:
        external_url = config.get(external_field_name)
        if external_url:
            return PictureReference(backend="url", id=str(external_url))

    value = config.get(field_name)
    if not isinstance(value, Mapping) or not value:
        return None
    if "backend" in value and "id" in value:
        try:
            return PictureReference.from_dict(value)
        except (TypeError, ValueError):
            return None
    if "model" in value and "pk" in value:
        return PictureReference(backend="filer", id=str(value["pk"]))
    return None


class ImageFormField(BackendImageField):
    """Backend image picker whose cleaned value is safe for a JSONField."""

    def __init__(self, *args, **kwargs):
        if kwargs.get("backends") is None:
            backends = list(get_backends())
            default_alias = getattr(settings, "DJANGOCMS_PICTURE_DEFAULT_BACKEND", "filer")
            backends.sort(key=lambda backend: backend.alias != default_alias)
            kwargs["backends"] = backends
        super().__init__(*args, **kwargs)

    def reference_from_selection(
        self,
        selection: BackendSelection | None,
    ) -> PictureReference | None:
        if selection is None:
            return None
        return selection.backend.serialize(selection.value)

    def selection_from_reference(
        self,
        reference: PictureReference,
    ) -> BackendSelection | None:
        backend = self.backends_by_alias.get(reference.backend)
        if backend is None:
            return None

        source_object = None
        if backend.stores_model_reference:
            asset = backend.resolve(reference)
            source_object = getattr(asset, "image", None) if asset else None
            if source_object is None:
                return BackendSelection(backend=backend, value=None)

        source = StoredPictureSource(
            backend=backend.alias,
            reference=reference,
            source_object=source_object,
        )
        holder = type("FrontendPictureSource", (), {"image_source": source})()
        try:
            value = backend.get_form_value(holder)
        except (ObjectDoesNotExist, TypeError, ValueError):
            value = None
        return BackendSelection(backend=backend, value=value)

    def prepare_value(self, value: Any) -> Any:
        if isinstance(value, Mapping):
            try:
                reference = PictureReference.from_dict(value)
            except (TypeError, ValueError):
                if "model" in value and "pk" in value:
                    reference = PictureReference(backend="filer", id=str(value["pk"]))
                else:
                    return value
            return self.selection_from_reference(reference)
        return value

    def clean(self, value: Any) -> dict[str, Any]:
        selection = super().clean(value)
        reference = self.reference_from_selection(selection)
        return reference.as_dict() if reference else {}

    def has_changed(self, initial: Any, data: Any) -> bool:
        if isinstance(initial, Mapping):
            initial = self.prepare_value(initial)
        if isinstance(data, BackendSelection):
            return super().has_changed(initial, data)
        return initial not in self.empty_values or data not in self.empty_values
