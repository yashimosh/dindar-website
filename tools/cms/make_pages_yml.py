#!/usr/bin/env python3
"""Writes .pages.yml (the Pages CMS config) at the repo root.

The editing forms are built from the real shape of tools/site/content_<loc>.json, so every
key in those files is a field (nothing can be dropped on save). Run it again after adding a
new section to the content files:

    python3 tools/cms/make_pages_yml.py

It refuses to write if the four languages do not have the same shape.
Standard library only.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
LOCS = [
    ("en", "English"),
    ("ku", "Kurdish (کوردی)"),
    ("ar", "Arabic (العربية)"),
    ("fa", "Persian (فارسی)"),
]

# Friendly names for the editing forms. Anything not listed gets its key, capitalised.
LABEL = {
    "nav_cta": "Menu button text",
    "hero": "Home page: top",
    "eyebrow": "Small line above the headline",
    "h1": "Headline",
    "p": "Text",
    "btn_work": "Button: my work",
    "btn_about": "Button: about me",
    "portrait_alt": "Portrait photo description",
    "stats": "Numbers",
    "n": "Number",
    "label": "Label",
    "body": "Text",
    "featured": "Featured work",
    "h2": "Section title",
    "sub": "Section subtitle",
    "items": "Items",
    "h3": "Title",
    "img": "Image file name (upload it under Photos first)",
    "alt": "Image description (for screen readers)",
    "tags": "Tags",
    "tag": "Tag",
    "cases": "Case studies",
    "name": "Name",
    "period": "Period",
    "metric": "Result",
    "campaigns": "Campaigns (YouTube)",
    "yt": "YouTube video ID (the part after v= in the link)",
    "yt_title": "Video title",
    "aria": "Label for screen readers",
    "thumb": "Thumbnail file name (upload it under Photos first)",
    "dur": "Duration",
    "note_pre": "Note: text before the link",
    "note_post": "Note: text after the link",
    "channel": "YouTube channel link",
    "text": "Text",
    "href": "Link",
    "reels": "Reels (Instagram)",
    "gallery": "Photo gallery",
    "certs": "Certificates",
    "issuer": "Issuer",
    "title": "Title",
    "description": "Description",
    "clients": "Clients: category names",
    "cats": "Categories (logos are edited under Client logos)",
    "logos": "Logos (read only: edit them under Client logos)",
    "file": "File",
    "expertise": "Core expertise",
    "icon": "Icon (one of: troubleshoot, campaign, hub, movie, trending_up)",
    "career": "Experience",
    "quote": "Quote",
    "role": "Role",
    "contact": "Contact section",
    "email_title": "Email box: title",
    "email_body": "Email box: text",
    "direct_title": "Direct contact box: title",
    "cta": "Closing call to action",
    "btn": "Button text",
    "footer": "Footer",
    "tagline": "Tagline",
    "copyright": "Copyright line",
    "h_languages": "Heading: languages",
    "h_sections": "Heading: sections",
    "h_inquiries": "Heading: inquiries",
    "start_project": "Button: Start a Project",
    "og_description": "Preview text on Facebook and WhatsApp",
    "tw_description": "Preview text on X (Twitter)",
    "og_locale": "Language code (do not change)",
    "mithra_title": "Mithra: job title",
    "mithra_org": "Mithra: company",
    "mithra_years": "Mithra: years",
    "mithra_body": "Mithra: text",
    "sales_title": "Sales: job title",
    "sales_org": "Sales: companies",
    "sales_years": "Sales: years",
    "sales_body": "Sales: text",
    "belief_label": "Belief: small label",
    "belief_title": "Belief: title",
    "belief_body": "Belief: text",
}
TOP_LABEL = {"meta": "Search engines and link previews"}  # 'meta' also exists inside certificates
SUMMARY_KEYS = ["h3", "name", "title", "n", "label", "issuer", "alt", "yt_title", "text"]
READONLY_KEYS = {"og_locale", "logos"}


def load(loc):
    with open(os.path.join(REPO, "tools", "site", f"content_{loc}.json"), encoding="utf-8") as f:
        return json.load(f)


def shape(o):
    if isinstance(o, dict):
        return {k: shape(v) for k, v in o.items()}
    if isinstance(o, list):
        return [shape(o[0])] if o else []
    return "str"


def q(s):
    return json.dumps(s, ensure_ascii=False)


def label_for(key, depth):
    if depth == 0 and key in TOP_LABEL:
        return TOP_LABEL[key]
    return LABEL.get(key, key.replace("_", " ").capitalize())


def is_long(samples):
    return any(len(v) > 70 or "\n" in v for v in samples)


def collect(values, path):
    """every language's value at this path, for choosing string vs text"""
    out = []
    for v in values:
        cur = v
        for p in path:
            cur = cur[0] if isinstance(cur, list) else cur
            cur = cur[p]
        out.append(cur)
    return out


def emit(key, val, indent, depth, docs, path, readonly):
    pad = " " * indent
    lines = [f"{pad}- name: {key}", f"{pad}  label: {q(label_for(key, depth))}"]
    ro = readonly or key in READONLY_KEYS
    if isinstance(val, dict):
        lines.append(f"{pad}  type: object")
        if ro and not readonly:
            lines.append(f"{pad}  readonly: true")
        lines.append(f"{pad}  fields:")
        for k, v in val.items():
            lines += emit(k, v, indent + 4, depth + 1, docs, path + [k], ro)
        return lines
    if isinstance(val, list):
        item = val[0] if val else "str"
        if isinstance(item, dict):
            summ = next((k for k in SUMMARY_KEYS if k in item), None)
            lines.append(f"{pad}  type: object")
            if ro and not readonly:
                lines.append(f"{pad}  readonly: true")
            lines.append(f"{pad}  list:")
            lines.append(f"{pad}    collapsible:")
            lines.append(f"{pad}      collapsed: true")
            lines.append(f"{pad}      summary: {q('{' + summ + '}') if summ else q('Item {index}')}")
            lines.append(f"{pad}  fields:")
            for k, v in item.items():
                lines += emit(k, v, indent + 4, depth + 1, docs, path + [k], ro)
        else:
            lines.append(f"{pad}  type: string")
            lines.append(f"{pad}  list: true")
        return lines
    samples = collect(docs, path)
    lines.append(f"{pad}  type: {'text' if is_long(samples) else 'string'}")
    if ro and not readonly:
        lines.append(f"{pad}  readonly: true")
    return lines


def main():
    docs = {l: load(l) for l, _ in LOCS}
    base = shape(docs["en"])
    for l, _ in LOCS:
        if shape(docs[l]) != base:
            raise SystemExit(f"content_{l}.json does not have the same shape as content_en.json; fix that first")
    values = [docs[l] for l, _ in LOCS]

    out = [
        "# Pages CMS config. GENERATED by tools/cms/make_pages_yml.py: change that script, not this file.",
        "# Forms come from tools/site/content_<language>.json; client logos from assets/data/clients.json.",
        "media:",
        "  - name: photos",
        "    label: Photos",
        "    input: assets/img",
        "    output: /assets/img",
        "    extensions: [jpg, jpeg, png, webp]",
        "    rename: safe",
        "  - name: logos",
        "    label: Client logos",
        "    input: assets/img/clients",
        "    output: /assets/img/clients",
        "    extensions: [webp, png]",
        "    rename: safe",
        "content:",
    ]
    for loc, name in LOCS:
        out += [
            f"  - name: text-{loc}",
            f"    label: {q('Website text: ' + name)}",
            "    type: file",
            f"    path: tools/site/content_{loc}.json",
            "    format: json",
            "    fields:",
        ]
        for k, v in docs[loc].items():
            out += emit(k, v, 6, 0, values, [k], False)
    out += [
        "  - name: client-logos",
        '    label: "Client logos"',
        "    type: file",
        "    path: assets/data/clients.json",
        "    format: json",
        "    fields:",
        "      - name: _readme",
        '        label: "How it works (read only)"',
        "        type: text",
        "        readonly: true",
        "      - name: alt",
        '        label: "Alt text template per language (read only)"',
        "        type: object",
        "        readonly: true",
        "        fields:",
    ]
    for loc, _ in LOCS:
        out += [f"          - name: {loc}", f'            label: "{loc}"', "            type: string"]
    out += [
        "      - name: alt_unnamed",
        '        label: "Alt text for logos without a name (read only)"',
        "        type: object",
        "        readonly: true",
        "        fields:",
    ]
    for loc, _ in LOCS:
        out += [f"          - name: {loc}", f'            label: "{loc}"', "            type: string"]
    out += [
        "      - name: categories",
        '        label: "Categories and their logos"',
        "        type: object",
        "        list:",
        "          collapsible:",
        "            collapsed: true",
        '            summary: "{id}"',
        "        fields:",
        "          - name: id",
        '            label: "Category id (do not change)"',
        "            type: string",
        "            readonly: true",
        "          - name: label",
        '            label: "Category name (read only: edit it under Website text > Clients)"',
        "            type: object",
        "            readonly: true",
        "            fields:",
    ]
    for loc, _ in LOCS:
        out += [f"              - name: {loc}", f'                label: "{loc}"', "                type: string"]
    out += [
        "          - name: sub",
        '            label: "Category subtitle (read only: edit it under Website text > Clients)"',
        "          " + "  type: object",
        "          " + "  readonly: true",
        "          " + "  fields:",
    ]
    for loc, _ in LOCS:
        out += [f"              - name: {loc}", f'                label: "{loc}"', "                type: string"]
    out += [
        "          - name: logos",
        '            label: "Logos (order here is the order on the site)"',
        "            type: object",
        "            list:",
        "              collapsible:",
        "                collapsed: true",
        '                summary: "{name}"',
        "            fields:",
        "              - name: name",
        '                label: "Brand name (leave empty if unknown)"',
        "                type: string",
        "              - name: file",
        '                label: "File: folder/name.webp (upload the image under Client logos first)"',
        "                type: string",
    ]
    path = os.path.join(REPO, ".pages.yml")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")
    print("wrote", path, len(out), "lines")


if __name__ == "__main__":
    main()
