# CellScribe - Bulk Excel to PDF Document Mail Merge

RowRender turns a Word template and an Excel sheet into personalised documents.
Write a letter once with placeholders like `[NAME]`, point RowRender at a sheet
of data, and it produces one finished document (optionally as a PDF) per row.

## Features

- Fills placeholders in the body, tables, headers and footers of a Word template
- One output document per Excel row, named from the columns you choose
- Optional PDF output
- `[DATE]` is automatically replaced with today's date
- Empty cells become `N/A` so a gap in the data is easy to spot

## Requirements

- Windows 10 or 11
- Microsoft Word, only if you want PDF output (the PDF step drives Word)
- Templates must be `.docx` and workbooks must be `.xlsx`

No .NET installation is needed. Releases are self-contained.

## Download

Get the latest `RowRender.exe` from the
[Releases page](https://github.com/steven-black/RowRender/releases). Because the source is public, you can also
build it yourself (see below).

## How to use

1. **Upload excel workbook** and enter the **name of the sheet** to use.
2. **Upload word template**. Put placeholders in it, e.g. `[NAME]`, `[AMOUNT]`.
3. Enter the **columns to use for naming**, separated by semicolons
   (e.g. `B;A`). Their values are joined with a space to name each file.
4. Enter an **output document name** and choose the **output folder**.
5. Click **Add placeholder and replacement** for each placeholder, and give the
   Excel column letter that holds its value (e.g. `[NAME]` → `A`).
6. Tick **Save as PDF** if you want PDFs, then click **Propagate**.

Output files are named `<naming columns>_<output document name>_<year>`.
If two rows would get the same name, the later ones are numbered
(`... (2)`, `... (3)`) instead of overwriting each other.

Every row in the sheet is processed, including the first, so a header row
produces a sample document that shows whether each column landed in the right place.

## Building from source

Requires the .NET 10 SDK on Windows.

```
git clone <repo url>
cd <repo folder>
dotnet run --project RowRender
```

Handy shortcuts are in `dev.sh` (`./dev.sh fresh`, `./dev.sh publish`).

## License

Copyright (C) 2026 Steven Black

RowRender is free software, licensed under the GNU General Public License v3.0.
See the [LICENSE](https://github.com/steven-black/RowRender/blob/main/LICENSE) file for the full text.

## Code signing policy

Free code signing provided by [SignPath.io](https://signpath.io), certificate by
[SignPath Foundation](https://signpath.org).

- Windows releases are built from this repository by GitHub Actions, and only
  those builds are submitted for signing.
- **Author and approver:** [Steven Black](https://github.com/steven-black)

This program does not collect or transmit any data. It reads the files you choose
and writes the documents you ask for on your own machine.
