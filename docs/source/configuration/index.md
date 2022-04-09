# Settings

The settings defined on this page allow you to better customize the behavior of the `chunky_upload` app.

## General Settings

| Name                              | Type                 | Default                      | Description                                                                                     |
| --------------------------------- | -------------------- | ---------------------------- | ----------------------------------------------------------------------------------------------- |
| `CHUNKED_UPLOAD_EXPIRATION_DELTA` | `datetime.timedelta` | `datetime.timedelta(days=1)` | Setups how long the `chunky_upload` is valid for                                                |
| `CHUNKED_UPLOAD_PATH`             | str                  | chunked_uploads/%Y/%m/%d     | Defines a path on in the file system that `chunky_upload` can be stored.                        |
| `CHUNKED_UPLOAD_STORAGE_CLASS`    | Storage_Class        | None                         | Defines the Django storage class that should be used for `chunky_upload`                        |
| `CHUNKED_UPLOAD_MAX_BYTES`        | int                  | None                         | Defines the maximum number of bytes that are allowed to be provided to `chunky_upload` at once. |
