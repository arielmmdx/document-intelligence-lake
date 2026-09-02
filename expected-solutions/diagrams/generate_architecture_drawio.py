#!/usr/bin/env python3
"""Write the single expected-architecture draw.io (no Lambda; Airflow orchestrates)."""

from pathlib import Path
from xml.sax.saxutils import escape

C_COMPUTE, C_STORAGE, C_DB = "#ED7100", "#3F8624", "#C925D1"
C_ANALYTICS, C_NET, C_INT = "#8C4FFF", "#8C4FFF", "#E7157B"
C_SEC, C_ML, C_MGMT, C_GEN = "#DD344C", "#01A88D", "#E7157B", "#232F3D"

ICON = (
    "sketch=0;outlineConnect=0;fontColor=#232F3E;fillColor={fill};strokeColor=#ffffff;"
    "dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;"
    "fontSize=10;fontStyle=0;aspect=fixed;shape=mxgraph.aws4.resourceIcon;"
    "resIcon=mxgraph.aws4.{res};fontFamily=Helvetica;labelBackgroundColor=#ffffff;"
)
AWS = (
    "points=[[0,0],[0.25,0,0],[0.5,0,0],[0.75,0,0],[1,0,0],[1,0.25,0],[1,0.5,0],"
    "[1,0.75,0],[1,1,0],[0.75,1,0],[0.5,1,0],[0.25,1,0],[0,1,0],[0,0.75,0],[0,0.5,0],"
    "[0,0.25,0]];outlineConnect=0;html=1;whiteSpace=wrap;fontSize=12;fontStyle=1;"
    "container=1;pointerEvents=0;collapsible=0;recursiveResize=0;shape=mxgraph.aws4.group;"
    "grIcon=mxgraph.aws4.group_aws_cloud;strokeColor=#232F3E;fillColor=none;"
    "verticalAlign=top;align=left;spacingLeft=30;fontColor=#232F3E;fontFamily=Helvetica;"
)
BAND = (
    "rounded=1;whiteSpace=wrap;html=1;verticalAlign=top;align=left;fontStyle=1;fontSize=12;"
    "fontFamily=Helvetica;container=1;collapsible=0;strokeWidth=2;spacingLeft=12;spacingTop=6;"
    "fillColor={fill};strokeColor={stroke};fontColor={stroke};"
)
COL = (
    "rounded=1;whiteSpace=wrap;html=1;verticalAlign=top;align=center;fontStyle=1;fontSize=11;"
    "fontFamily=Helvetica;container=1;collapsible=0;strokeWidth=2;spacingTop=8;"
    "fillColor={fill};strokeColor={stroke};fontColor={stroke};"
)
TASK = (
    "rounded=1;whiteSpace=wrap;html=1;align=center;verticalAlign=middle;fontSize=10;"
    "fontStyle=1;fontFamily=Helvetica;fillColor={fill};strokeColor={stroke};fontColor=#232F3E;"
    "arcSize=12;strokeWidth=2;"
)
EDGE = (
    "endArrow=block;endFill=1;html=1;rounded=0;strokeColor=#232F3E;strokeWidth=2;"
    "edgeStyle=orthogonalEdgeStyle;exitX=1;exitY=0.5;exitDx=0;exitDy=0;"
    "entryX=0;entryY=0.5;entryDx=0;entryDy=0;jumpStyle=arc;jumpSize=6;"
)
LEG = (
    "text;html=1;align=left;verticalAlign=top;fontSize=11;fontFamily=Helvetica;"
    "whiteSpace=wrap;overflow=hidden;fontColor=#232F3E;"
)


def cell(cid, value, style, x, y, w, h, parent="1", html=False):
    if not value:
        val = ""
    elif html:
        val = value.replace('"', "&quot;")
    else:
        val = escape(value).replace("\n", "&#xa;")
    return (
        f'        <mxCell id="{cid}" value="{val}" style="{style}" vertex="1" parent="{parent}">\n'
        f'          <mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry" />\n'
        f"        </mxCell>\n"
    )


def icon(cid, parent, x, y, res, fill, label):
    return cell(cid, label, ICON.format(fill=fill, res=res), x, y, 48, 48, parent)


def edge(eid, src, tgt):
    return (
        f'        <mxCell id="{eid}" value="" style="{EDGE}" edge="1" parent="airflow" '
        f'source="{src}" target="{tgt}">\n'
        f'          <mxGeometry relative="1" as="geometry" />\n'
        f"        </mxCell>\n"
    )


def build():
    p = []
    p.append(cell("title", "Document Intelligence Lake — expected solution",
                  "text;html=1;align=left;fontSize=26;fontStyle=1;fontFamily=Helvetica;fontColor=#232F3E;",
                  40, 16, 900, 36))
    p.append(cell("sub", "Apache Airflow (Amazon MWAA) orchestrates the DAG. ECS runs Python. Glue runs PySpark. No Lambda.",
                  "text;html=1;align=left;fontSize=13;fontFamily=Helvetica;fontColor=#545B64;",
                  40, 52, 1100, 22))
    p.append(cell("line", "", "line;strokeWidth=3;strokeColor=#FF9900;", 40, 78, 1920, 8))

    p.append(cell("aws", "AWS Cloud  ·  eu-west-1", AWS, 40, 100, 1460, 1040))

    p.append(cell("airflow", "Orchestration — Amazon MWAA (Apache Airflow)",
                  BAND.format(fill="#FCE4EC", stroke="#E7157B"), 24, 40, 1412, 200, "aws"))
    p.append(icon("i-mwaa", "airflow", 16, 88, "managed_workflows_apache_airflow", C_INT, "MWAA"))

    tasks = [
        ("t1", "T1\nS3 sensor", "#FFEBEE", "#C62828"),
        ("t2", "T2\nClassify", "#FFF8E1", "#F9A825"),
        ("t3", "T3\nBranch", "#FFF8E1", "#F9A825"),
        ("t4", "T4\nExtract", "#FFF3E0", "#E65100"),
        ("t5", "T5\nSilver", "#E3F2FD", "#1565C0"),
        ("t6", "T6\nGold", "#E8F5E9", "#2E7D32"),
        ("t7", "T7\nPublish", "#F3E5F5", "#6A1B9A"),
    ]
    x0 = 100
    for i, (tid, label, fill, stroke) in enumerate(tasks):
        p.append(cell(tid, label, TASK.format(fill=fill, stroke=stroke), x0 + i * 184, 78, 168, 72, "airflow"))
    for i in range(6):
        p.append(edge(f"ae{i}", tasks[i][0], tasks[i + 1][0]))

    p.append(cell("plane", "Data plane — workers the DAG starts (not Airflow itself)",
                  BAND.format(fill="#FAFAFA", stroke="#545B64"), 24, 260, 1412, 500, "aws"))

    cols = [
        ("c1", "Landing", "#FFEBEE", "#C62828", 16, [
            ("sftp", "transfer_family", C_STORAGE, "Transfer Family"),
            ("s3l", "s3", C_STORAGE, "S3 landing"),
            ("s3q", "s3", C_STORAGE, "S3 quarantine"),
        ]),
        ("c2", "Bronze", "#FFF8E1", "#F9A825", 294, [
            ("ecs-c", "fargate", C_COMPUTE, "ECS Python\nclassify"),
            ("s3b", "s3", C_STORAGE, "S3 inventory"),
            ("ddb", "dynamodb", C_DB, "Doc + contract\nregistry"),
        ]),
        ("c3", "Extract workers", "#FFF3E0", "#E65100", 572, [
            ("tex", "textract", C_ML, "Textract\npage batches"),
            ("ecs-e", "ecs", C_COMPUTE, "ECS Python\nmapped tasks"),
            ("glue-e", "glue", C_ANALYTICS, "Glue PySpark\nlarge Excel"),
        ]),
        ("c4", "Silver + gold", "#E8F5E9", "#2E7D32", 850, [
            ("s3s", "s3", C_STORAGE, "S3 silver\nIceberg"),
            ("s3g", "s3", C_STORAGE, "S3 gold\nIceberg"),
            ("cat", "data_catalog", C_ANALYTICS, "Glue Catalog\n+ Lake Formation"),
        ]),
        ("c5", "Serve", "#F3E5F5", "#6A1B9A", 1128, [
            ("ath", "athena", C_ANALYTICS, "Athena"),
            ("qs", "quicksight", C_ANALYTICS, "QuickSight /\nTableau"),
            ("pdf", "fargate", C_COMPUTE, "ECS PDF render\nfrom gold"),
        ]),
    ]
    for cid, title, fill, stroke, x, icons in cols:
        p.append(cell(cid, title, COL.format(fill=fill, stroke=stroke), x, 44, 262, 430, "plane"))
        for j, (iid, res, col, lab) in enumerate(icons):
            p.append(icon(iid, cid, 107, 70 + j * 120, res, col, lab))

    p.append(cell("sec", "Control plane — identity, keys, images, audit (not a data layer)",
                  BAND.format(fill="#FFEBEE", stroke="#DD344C"), 24, 780, 1412, 220, "aws"))
    sec_icons = [
        ("sso", "iam_identity_center", C_SEC, "Identity Center\nSSO + MFA"),
        ("iam", "identity_and_access_management", C_SEC, "IAM roles\nper worker"),
        ("kms", "kms", C_SEC, "KMS CMK\nper zone"),
        ("ecr", "ecr", C_COMPUTE, "ECR\nPython images"),
        ("cw", "cloudwatch", C_MGMT, "CloudWatch\nno PII"),
        ("ct", "cloudtrail", C_MGMT, "CloudTrail"),
        ("ep", "endpoints", C_NET, "VPC endpoints"),
        ("lf", "lake_formation", C_ANALYTICS, "Lake Formation"),
    ]
    for i, (iid, res, fill, lab) in enumerate(sec_icons):
        p.append(icon(iid, "sec", 40 + i * 170, 80, res, fill, lab))

    # Right legend — text only, no crossing lines
    p.append(cell("legbox", "",
                  "rounded=1;whiteSpace=wrap;html=1;fillColor=#F7F9FC;strokeColor=#6c8ebf;container=1;collapsible=0;verticalAlign=top;align=left;fontStyle=1;fontSize=13;fontFamily=Helvetica;spacingLeft=14;spacingTop=10;",
                  1520, 100, 440, 1040))
    p.append(cell("legt", "How to read this diagram",
                  "text;html=1;align=left;fontSize=16;fontStyle=1;fontFamily=Helvetica;",
                  16, 12, 400, 28, "legbox"))
    legend = (
        "<b>T1</b> Sensor waits on S3 landing. "
        "Checksum becomes the DAG idempotency key.<br><br>"
        "<b>T2–T3</b> ECS Python classifier. "
        "Branch: PDF, Excel, SQLite/Word, or quarantine.<br><br>"
        "<b>T4</b> Workers, never the MWAA node. "
        "Mapped ECS + Textract for huge PDFs. "
        "Glue PySpark for large Excel. "
        "Python paging for SQLite.<br><br>"
        "<b>T5–T6</b> Glue PySpark writes Iceberg silver then gold. "
        "Types, PII tags, tenant_id, layout_version.<br><br>"
        "<b>T7</b> Atomic snapshot. Then Athena / BI / PDF-from-gold.<br><br>"
        "<b>AI</b> drafts a JSON contract (sample pages). "
        "ECR interpreter applies it. No exec of generated Python.<br><br>"
        "<b>Lines</b> exist only on the Airflow row so labels never sit on arrows."
    )
    p.append(cell("legb", legend, LEG, 16, 48, 408, 960, "legbox", html=True))
    return "".join(p)


def main():
    inner = build()
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<mxfile host="app.diagrams.net" agent="G2i Document Intelligence Lake" version="22.1.16">\n'
        '  <diagram id="expected" name="Expected architecture">\n'
        '    <mxGraphModel dx="1400" dy="900" grid="1" gridSize="10" guides="1" tooltips="1" '
        'connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="2000" pageHeight="1200" '
        'math="0" shadow="0">\n'
        "      <root>\n"
        '        <mxCell id="0" />\n'
        '        <mxCell id="1" parent="0" />\n'
        f"{inner}"
        "      </root>\n"
        "    </mxGraphModel>\n"
        "  </diagram>\n"
        "</mxfile>\n"
    )
    out = Path(__file__).resolve().parent / "01_expected_architecture.drawio"
    out.write_text(xml, encoding="utf-8")
    print(f"wrote {out} ({len(xml)} bytes)")


if __name__ == "__main__":
    main()
