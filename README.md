# r-subsync
Script to recursively sync (using ![Subsync](https://github.com/smacke/subsync)) all the subtitles of a folder and overwrite the old one (after backing it up). It won't try to sync previously synced subs on next iterations.

# Requirements
- Python 3.6+
- ![Subsync](https://github.com/smacke/subsync)

# Example usage
Having:

```
.
└── path-to-sync-recursively
    ├── video1
    │   ├── video1.en.srt
    │   └── video1.mkv
    └── video2
        ├── video2.en.srt
        └── video2.mkv
```
Using the command:

`python3 rSubsync.py --lang en --path /path-to-sync-recursively/`

Will do this:

```
.
└── path-to-sync-recursively
    ├── video1
    │   ├── video1.en.srt
    │   ├── video1.en.srt.old
    │   └── video1.mkv
    └── video2
        ├── video2.en.srt
        ├── video2.en.srt.old
        └── video2.mkv
```

In case there are errors in the process of syncing any subtitle, it will create a `.failed` file with the stacktrace.
