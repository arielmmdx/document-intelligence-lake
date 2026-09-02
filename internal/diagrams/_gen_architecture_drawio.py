#!/usr/bin/env python3
"""Generate AWS-icon architecture.drawio. Run from repo; writes candidate + internal copies."""

from pathlib import Path
from xml.sax.saxutils import escape

# AWS resourceIcon category fills
C_COMPUTE = "#ED7100"
C_STORAGE = "#3F8624"
C_DB = "#C925D1"
C_ANALYTICS = "#8C4FFF"
C_NET = "#8C4FFF"
C_INT = "#E7157B"
C_SEC = "#DD344C"
C_ML = "#01A88D"
C_MGMT = "#E7157B"
C_GEN = "#232F3D"

ICON = (
    "sketch=0;outlineConnect=0;fontColor=#232F3E;fillColor={fill};strokeColor=#ffffff;"
    "dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;"
    "fontSize=10;fontStyle=0;aspect=fixed;shape=mxgraph.aws4.resourceIcon;"
    "resIcon=mxgraph.aws4.{res};fontFamily=Helvetica;"
)
GROUP_AWS = (
    "points=[[0,0],[0.25,0,0],[0.5,0,0],[0.75,0,0],[1,0,0],[1,0.25,0],[1,0.5,0],"
    "[1,0.75,0],[1,1,0],[0.75,1,0],[0.5,1,0],[0.25,1,0],[0,1,0],[0,0.75,0],[0,0.5,0],"
    "[0,0.25,0]];outlineConnect=0;gradientColor=none;html=1;whiteSpace=wrap;fontSize=12;"
    "fontStyle=1;container=1;pointerEvents=0;collapsible=0;recursiveResize=0;"
    "shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_aws_cloud;strokeColor=#232F3E;"
    "fillColor=none;verticalAlign=top;align=left;spacingLeft=30;fontColor=#232F3E;dashed=0;"
    "fontFamily=Helvetica;"
)
GROUP_REGION = (
    "points=[[0,0],[0.25,0,0],[0.5,0,0],[0.75,0,0],[1,0,0],[1,0.25,0],[1,0.5,0],"
    "[1,0.75,0],[1,1,0],[0.75,1,0],[0.5,1,0],[0.25,1,0],[0,1,0],[0,0.75,0],[0,0.5,0],"
    "[0,0.25,0]];outlineConnect=0;gradientColor=none;html=1;whiteSpace=wrap;fontSize=12;"
    "fontStyle=1;container=1;pointerEvents=0;collapsible=0;recursiveResize=0;"
    "shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_region;strokeColor=#00A4A6;"
    "fillColor=none;verticalAlign=top;align=left;spacingLeft=30;fontColor=#147EBA;dashed=1;"
    "dashPattern=8 4;fontFamily=Helvetica;"
)
GROUP_VPC = (
    "points=[[0,0],[0.25,0,0],[0.5,0,0],[0.75,0,0],[1,0,0],[1,0.25,0],[1,0.5,0],"
    "[1,0.75,0],[1,1,0],[0.75,1,0],[0.5,1,0],[0.25,1,0],[0,1,0],[0,0.75,0],[0,0.5,0],"
    "[0,0.25,0]];outlineConnect=0;gradientColor=none;html=1;whiteSpace=wrap;fontSize=12;"
    "fontStyle=1;container=1;pointerEvents=0;collapsible=0;recursiveResize=0;"
    "shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_vpc;strokeColor=#8C4FFF;"
    "fillColor=#F4F0FF;verticalAlign=top;align=left;spacingLeft=30;fontColor=#8C4FFF;"
    "dashed=0;fontFamily=Helvetica;"
)
LANE = (
    "rounded=0;whiteSpace=wrap;html=1;verticalAlign=top;align=center;fontStyle=1;"
    "fontSize=11;fontFamily=Helvetica;container=1;collapsible=0;strokeWidth=2;"
    "arcSize=8;fillColor={fill};strokeColor={stroke};fontColor={stroke};spacingTop=4;"
)
NOTE = (
    "shape=note;whiteSpace=wrap;html=1;align=left;spacingLeft=8;spacingTop=4;"
    "size=16;fillColor=#FFFDE7;strokeColor=#F9A825;fontSize=10;fontFamily=Helvetica;"
)
EDGE = (
    "edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;"
    "html=1;endArrow=block;endFill=1;strokeColor=#232F3E;strokeWidth=1.5;"
    "fontFamily=Helvetica;fontSize=9;fontColor=#232F3E;"
)
TITLE = "text;html=1;align=left;verticalAlign=middle;fontSize=28;fontStyle=1;fontFamily=Helvetica;fontColor=#232F3E;"
SUB = "text;html=1;align=left;verticalAlign=middle;fontSize=14;fontFamily=Helvetica;fontColor=#545B64;"
LINE = "line;strokeWidth=3;html=1;strokeColor=#FF9900;"
TXT = "text;html=1;align=left;verticalAlign=top;fontSize=11;fontFamily=Helvetica;whiteSpace=wrap;overflow=hidden;fontColor=#232F3E;"


def cell(cid, value, style, x, y, w, h, parent="1", vertex=True):
    val = escape(value).replace("\n", "&#xa;") if value else ""
    return (
        f'        <mxCell id="{cid}" value="{val}" style="{style}" vertex="1" parent="{parent}">\n'
        f'          <mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry" />\n'
        f"        </mxCell>\n"
    )


def icon(cid, parent, x, y, res, fill, label, size=48):
    return cell(cid, label, ICON.format(fill=fill, res=res), x, y, size, size, parent)


def edge(eid, src, tgt, label=""):
    val = escape(label) if label else ""
    extra = "verticalAlign=bottom;align=center;" if label else ""
    return (
        f'        <mxCell id="{eid}" value="{val}" style="{EDGE}{extra}" edge="1" parent="1" source="{src}" target="{tgt}">\n'
        f'          <mxGeometry relative="1" as="geometry" />\n'
        f"        </mxCell>\n"
    )


def page1():
    p = []
    p.append(cell("t1", "Document Intelligence Lake — medallion on AWS", TITLE, 40, 16, 1100, 36))
    p.append(cell("t2", "eu-west-1 · ingest → bronze → layout/extract → silver → gold → serve · PII zones isolated", SUB, 40, 52, 1400, 24))
    p.append(cell("t3", "", LINE, 40, 80, 2280, 8))

    # Producers
    p.append(cell("g-src", "Producers", LANE.format(fill="#F5F5F5", stroke="#545B64"), 40, 110, 160, 520))
    p.append(icon("i-users", "g-src", 56, 50, "users", C_GEN, "Customers / scanners"))
    p.append(icon("i-xfer", "g-src", 56, 160, "transfer_family", C_STORAGE, "Transfer Family\nSFTP/HTTPS"))
    p.append(icon("i-api-in", "g-src", 56, 280, "api_gateway", C_NET, "API Gateway\nupload API"))
    p.append(icon("i-ext", "g-src", 56, 400, "user", C_GEN, "Ops / legal hold"))

    p.append(cell("g-aws", "AWS Cloud", GROUP_AWS, 210, 100, 2000, 1180))
    p.append(cell("g-reg", "Region eu-west-1", GROUP_REGION, 16, 40, 1968, 1120, "g-aws"))

    # Control plane top
    p.append(cell(
        "g-ctrl",
        "Control / security plane (cross-cutting — not a data layer)",
        LANE.format(fill="#FFEBEE", stroke="#DD344C"),
        16, 40, 1936, 150,
        "g-reg",
    ))
    p.append(icon("i-sso", "g-ctrl", 30, 40, "iam_identity_center", C_SEC, "IAM Identity Center\nSSO + MFA"))
    p.append(icon("i-iam", "g-ctrl", 200, 40, "identity_and_access_management", C_SEC, "IAM task roles\nleast privilege"))
    p.append(icon("i-kms", "g-ctrl", 370, 40, "kms", C_SEC, "KMS CMKs\nper data zone"))
    p.append(icon("i-secm", "g-ctrl", 540, 40, "secrets_manager", C_SEC, "Secrets Manager"))
    p.append(icon("i-trail", "g-ctrl", 710, 40, "cloudtrail", C_MGMT, "CloudTrail\naudit"))
    p.append(icon("i-cw", "g-ctrl", 880, 40, "cloudwatch", C_MGMT, "CloudWatch\nno PII in logs"))
    p.append(icon("i-macie", "g-ctrl", 1050, 40, "macie", C_SEC, "Macie\nraw-zone scan"))
    p.append(icon("i-vpce", "g-ctrl", 1220, 40, "endpoints", C_NET, "VPC endpoints\nS3/ECR/Glue"))
    p.append(icon("i-waf", "g-ctrl", 1390, 40, "waf", C_SEC, "WAF\nupload + API"))
    p.append(icon("i-ecr", "g-ctrl", 1560, 40, "ecr", C_COMPUTE, "ECR\nscanned images"))
    p.append(icon("i-eb", "g-ctrl", 1730, 40, "eventbridge", C_INT, "EventBridge\nS3 events"))

    # Medallion lanes
    y0 = 210
    h_lane = 720
    lanes = [
        ("g-land", "1  LANDING  ·  raw", "#FFEBEE", "#C62828", 20,
         "Immutable bytes. Object Lock. Same trust as PII source. Not for analysts."),
        ("g-brz", "2  BRONZE  ·  inventory", "#FFF8E1", "#F9A825", 295,
         "Catalog of objects + derivatives (Textract JSON). Still raw-class. Query metadata, not business facts."),
        ("g-lay", "3  LAYOUT / AI", "#E0F2F1", "#00796B", 570,
         "Discover or reuse a versioned extraction contract. AI on samples only — not exec(Python)."),
        ("g-ext", "4  EXTRACT compute", "#FFF3E0", "#E65100", 845,
         "Trusted runtime applies the contract. Route ECS vs Glue vs Textract by format and size."),
        ("g-sil", "5  SILVER  ·  conformed", "#E3F2FD", "#1565C0", 1120,
         "Typed Parquet/Iceberg. Grain = extracted entity/page/line. PII tags + layout_version + lineage."),
        ("g-gld", "6  GOLD  ·  business", "#E8F5E9", "#2E7D32", 1395,
         "Dimensional / entity model. Published snapshot only. Lake Formation tenant row filters."),
        ("g-srv", "7  SERVE", "#F3E5F5", "#6A1B9A", 1670,
         "Athena / BI / regenerated PDF / website. Gold is source of truth — never landing PDFs."),
    ]
    for gid, title, fill, stroke, x, _note in lanes:
        p.append(cell(gid, title, LANE.format(fill=fill, stroke=stroke), x, y0, 265, h_lane, "g-reg"))

    # Landing icons
    p.append(icon("i-s3l", "g-land", 111, 50, "s3", C_STORAGE, "S3 landing\nObject Lock + CMK-raw"))
    p.append(icon("i-s3q", "g-land", 111, 160, "s3", C_STORAGE, "S3 quarantine\nsame class as raw"))
    p.append(icon("i-lam", "g-land", 111, 270, "lambda", C_COMPUTE, "Lambda ingest\nchecksum / tenant"))
    p.append(icon("i-sfn0", "g-land", 111, 380, "step_functions", C_INT, "Step Functions\norchestrator"))
    p.append(cell("n-land", "Unit of ingest = object.\nIdempotent on tenant+checksum.\nNever mutate; never crawl for BI.", NOTE, 20, 500, 230, 90, "g-land"))

    # Bronze
    p.append(icon("i-ecs-c", "g-brz", 111, 50, "fargate", C_COMPUTE, "ECS Fargate\nclassifier"))
    p.append(icon("i-s3b", "g-brz", 111, 160, "s3", C_STORAGE, "S3 bronze\ninventory + OCR JSON"))
    p.append(icon("i-glueb", "g-brz", 111, 270, "data_catalog", C_ANALYTICS, "Glue Catalog\nbronze_inventory"))
    p.append(icon("i-ddb-id", "g-brz", 111, 380, "dynamodb", C_DB, "DynamoDB\ndoc registry / leases"))
    p.append(cell("n-brz", "Classifier: MIME, scanned vs digital,\npage count, encryption, size.\nWrites metadata, not a second PDF copy.", NOTE, 20, 500, 230, 90, "g-brz"))

    # Layout
    p.append(icon("i-tex", "g-lay", 40, 50, "textract", C_ML, "Textract Analyze\nsample pages"))
    p.append(icon("i-bed", "g-lay", 150, 50, "bedrock", C_ML, "Bedrock\ncontract draft"))
    p.append(icon("i-ddbc", "g-lay", 111, 170, "dynamodb", C_DB, "Contract registry\nfingerprint → version"))
    p.append(icon("i-s3a", "g-lay", 111, 280, "s3", C_STORAGE, "S3 artifacts\ncontracts JSON"))
    p.append(icon("i-gt", "g-lay", 111, 390, "sagemaker_ground_truth", C_ML, "Human gate\napprove contract"))
    p.append(cell("n-lay", "Stratified sample (not only first 20).\nMismatch mid-doc → split or quarantine.\nPromote interpreter via ECR digest.", NOTE, 20, 500, 230, 90, "g-lay"))

    # Extract
    p.append(icon("i-ecs-e", "g-ext", 40, 50, "ecs", C_COMPUTE, "ECS Fargate\nPython interpreter"))
    p.append(icon("i-gluej", "g-ext", 150, 50, "glue", C_ANALYTICS, "Glue Spark job\nlarge Excel/CSV"))
    p.append(icon("i-tex2", "g-ext", 40, 170, "textract", C_ML, "Textract async\npage batches"))
    p.append(icon("i-sfn1", "g-ext", 150, 170, "step_functions", C_INT, "Map state\n50-page units"))
    p.append(icon("i-sqs", "g-ext", 111, 290, "simple_queue_service", C_INT, "SQS\nwork + DLQ"))
    p.append(icon("i-emr", "g-ext", 111, 390, "emr", C_ANALYTICS, "EMR (optional)\nif Glue DPUs not enough"))
    p.append(cell("n-ext", "PDF huge → SFN + Textract.\nExcel huge → Glue.\nSQLite → paged ECS worker.\nNo LLM credentials on silver.", NOTE, 20, 500, 230, 90, "g-ext"))

    # Silver
    p.append(icon("i-s3s", "g-sil", 111, 50, "s3", C_STORAGE, "S3 silver\nIceberg/Parquet + CMK"))
    p.append(icon("i-glues", "g-sil", 111, 160, "glue", C_ANALYTICS, "Glue job\nstaging → verify"))
    p.append(icon("i-cats", "g-sil", 111, 270, "data_catalog", C_ANALYTICS, "Glue Catalog\nsilver tables"))
    p.append(icon("i-ice", "g-sil", 111, 380, "athena", C_ANALYTICS, "Iceberg snapshot\natomic publish gate"))
    p.append(cell("n-sil", "Columns: tenant_id, document_id,\npage_range, layout_version, pii_class,\nsource_uri, extraction_job_id.\nAnalysts: LF-filtered only.", NOTE, 20, 500, 230, 90, "g-sil"))

    # Gold
    p.append(icon("i-s3g", "g-gld", 111, 50, "s3", C_STORAGE, "S3 gold\nentity / star schema"))
    p.append(icon("i-glueg", "g-gld", 111, 160, "glue", C_ANALYTICS, "Glue Spark\nconformed model"))
    p.append(icon("i-lf", "g-gld", 111, 270, "lake_formation", C_ANALYTICS, "Lake Formation\nrow/column filters"))
    p.append(icon("i-catg", "g-gld", 111, 380, "data_catalog", C_ANALYTICS, "Glue Catalog\ngold database"))
    p.append(cell("n-gld", "Business grain (claim, line, shipment).\nCross-format keys per tenant.\nPublish after independent checks.", NOTE, 20, 500, 230, 90, "g-gld"))

    # Serve
    p.append(icon("i-ath", "g-srv", 40, 50, "athena", C_ANALYTICS, "Athena\nworkgroup / tenant"))
    p.append(icon("i-qs", "g-srv", 150, 50, "quicksight", C_ANALYTICS, "QuickSight\nor Tableau/PBI"))
    p.append(icon("i-apig", "g-srv", 40, 170, "api_gateway", C_NET, "API Gateway\nwebsite BFF"))
    p.append(icon("i-cog", "g-srv", 150, 170, "cognito", C_SEC, "Cognito\napp auth (SSO)"))
    p.append(icon("i-pdf", "g-srv", 40, 290, "fargate", C_COMPUTE, "ECS render\nPDF from gold"))
    p.append(icon("i-s3p", "g-srv", 150, 290, "s3", C_STORAGE, "S3 serving-pdf\nshort retention OK"))
    p.append(cell("n-srv", "Tableau → Athena connector on gold.\nWebsite never presigns landing.\nPDF reprint uses tagged gold fields.", NOTE, 20, 500, 230, 90, "g-srv"))

    # Consumers
    p.append(cell("g-cons", "Consumers", LANE.format(fill="#E8EAF6", stroke="#3F51B5"), 2220, 110, 160, 520, "1"))
    p.append(icon("i-ana", "g-cons", 56, 50, "user", C_GEN, "Analysts\nSSO"))
    p.append(icon("i-tab", "g-cons", 56, 160, "quicksight", C_ANALYTICS, "Tableau /\nPower BI"))
    p.append(icon("i-web", "g-cons", 56, 280, "internet", C_NET, "Customer\nwebsite"))
    p.append(icon("i-legal", "g-cons", 56, 400, "organizations", C_MGMT, "Legal / audit\nbreak-glass"))

    # Flow edges between layer icons (connect across groups — source/target must be vertices)
    p.append(edge("e1", "i-xfer", "i-s3l", "put object"))
    p.append(edge("e2", "i-api-in", "i-s3l"))
    p.append(edge("e3", "i-s3l", "i-eb", "ObjectCreated"))
    p.append(edge("e4", "i-eb", "i-sfn0"))
    p.append(edge("e5", "i-sfn0", "i-ecs-c"))
    p.append(edge("e6", "i-ecs-c", "i-s3b"))
    p.append(edge("e7", "i-ecs-c", "i-s3q", "unknown / poison"))
    p.append(edge("e8", "i-s3b", "i-ddbc", "fingerprint"))
    p.append(edge("e9", "i-ddbc", "i-tex", "unknown layout"))
    p.append(edge("e10", "i-bed", "i-s3a", "contract JSON"))
    p.append(edge("e11", "i-s3a", "i-ecs-e", "pin digest"))
    p.append(edge("e12", "i-sfn1", "i-tex2"))
    p.append(edge("e13", "i-ecs-e", "i-s3s"))
    p.append(edge("e14", "i-gluej", "i-s3s"))
    p.append(edge("e15", "i-tex2", "i-s3s"))
    p.append(edge("e16", "i-s3s", "i-glueg"))
    p.append(edge("e17", "i-glueg", "i-s3g"))
    p.append(edge("e18", "i-lf", "i-ath"))
    p.append(edge("e19", "i-ath", "i-qs"))
    p.append(edge("e20", "i-ath", "i-apig"))
    p.append(edge("e21", "i-s3g", "i-pdf"))
    p.append(edge("e22", "i-pdf", "i-s3p"))
    p.append(edge("e23", "i-qs", "i-tab"))
    p.append(edge("e24", "i-apig", "i-web"))
    p.append(edge("e25", "i-sso", "i-ana", "permission sets"))

    p.append(cell(
        "foot",
        "Medallion rule: quality and access increase left → right; sensitivity of raw bytes stays in landing/bronze/quarantine. "
        "Silver/gold are derived tables with KMS and Lake Formation. Publish is an Iceberg snapshot (or equivalent manifest), not a copy into current/.",
        TXT, 220, 1310, 1900, 40,
    ))
    return "".join(p)


def page2():
    """Layer dictionary — what lives in each medallion layer."""
    p = []
    p.append(cell("p2t", "Medallion layers — what belongs where", TITLE, 40, 16, 900, 36))
    p.append(cell("p2s", "Each layer has a different contract, CMK, IAM role, and consumer. Do not collapse them into one bucket.", SUB, 40, 52, 1400, 24))
    p.append(cell("p2l", "", LINE, 40, 80, 1800, 8))

    blocks = [
        (100, "#FFEBEE", "#C62828", "Landing (raw)",
         "<b>Purpose.</b> Keep the original file forever (legal hold / Object Lock).<br>"
         "<b>Contents.</b> PDF/Excel/Word/SQLite/text as uploaded. Checksum, tenant prefix, content-type metadata.<br>"
         "<b>AWS.</b> S3 landing, Transfer Family, API Gateway, Lambda checksum, EventBridge, KMS-raw, optional Macie.<br>"
         "<b>Who.</b> ingest-task-role write; break-glass read. <b>Not</b> Athena analysts.<br>"
         "<b>Success.</b> Object stored once, immutable, accounted for."),
        (280, "#FFF8E1", "#F9A825", "Bronze",
         "<b>Purpose.</b> Make the lake <i>operable</i>: what arrived, in what shape, is it scanned, how many pages.<br>"
         "<b>Contents.</b> Inventory table; optional Textract JSON / page images as derivatives (still raw-class).<br>"
         "<b>AWS.</b> ECS Fargate classifier, DynamoDB doc registry, Glue Data Catalog bronze_inventory, S3 bronze prefix, quarantine bucket.<br>"
         "<b>Who.</b> classifier and layout roles. Still not a BI source.<br>"
         "<b>Success.</b> Every landing object has a row; poison goes to quarantine with a reason code."),
        (460, "#E0F2F1", "#00796B", "Layout intelligence (between bronze and silver)",
         "<b>Purpose.</b> Compress 10k pages into a reusable <i>extraction contract</i> (not generated Python in prod).<br>"
         "<b>Contents.</b> Fingerprint, contract JSON, human approval record, pinned ECR digest of the interpreter.<br>"
         "<b>AWS.</b> Textract Analyze on stratified samples, Bedrock for draft mapping, DynamoDB registry, S3 artifacts, Ground Truth / review UI.<br>"
         "<b>Who.</b> layout-task-role; reviewers via SSO. Model cannot PutObject to silver.<br>"
         "<b>Success.</b> Known forms skip AI; unknown forms emit a versioned contract; drift mid-document splits work."),
        (640, "#FFF3E0", "#E65100", "Extract (compute that writes silver)",
         "<b>Purpose.</b> Apply the contract in bounded, retryable units.<br>"
         "<b>Routing.</b> ECS Python (small docs, SQLite paging) · Step Functions map + Textract async (huge/scanned PDF) · Glue Spark (large Excel/CSV) · EMR only if Glue is not enough.<br>"
         "<b>AWS.</b> ECR images, ECS/Fargate, SQS + DLQ, Glue jobs, optional EMR, KMS data keys cached at job grain (not per page).<br>"
         "<b>Success.</b> Staging prefix per run_id; retries idempotent; tables spanning pages use overlap + reduce."),
        (820, "#E3F2FD", "#1565C0", "Silver",
         "<b>Purpose.</b> Conformed, typed, queryable facts with lineage to page/object.<br>"
         "<b>Grain examples.</b> form instance, table row, text chunk — declared per contract. Always tenant_id + layout_version + pii_class.<br>"
         "<b>AWS.</b> S3 silver (Iceberg), Glue job verify, Glue Catalog, Lake Formation optional at this layer.<br>"
         "<b>Who.</b> extractor/glue-extract-role write staging; publish role commits snapshot; analysts only if LF allows.<br>"
         "<b>Success.</b> Independent verification of serialized files; no partial current/ folder."),
        (1000, "#E8F5E9", "#2E7D32", "Gold",
         "<b>Purpose.</b> Business entities and metrics for consumption (claim, shipment, invoice line).<br>"
         "<b>Contents.</b> Conformed keys across PDF and Excel; slowly changing layout handled as versioned attributes.<br>"
         "<b>AWS.</b> Glue Spark model job, S3 gold, Glue Catalog gold DB, Lake Formation grants, KMS-gold.<br>"
         "<b>Who.</b> glue-model-role write; athena-analyst-role and Tableau role read via LF.<br>"
         "<b>Success.</b> One published snapshot Athena can see; previous snapshot remains readable."),
        (1180, "#F3E5F5", "#6A1B9A", "Serve (not a medallion layer — consumption)",
         "<b>Purpose.</b> SQL, BI, regenerated PDF, website — all from gold (or approved silver views).<br>"
         "<b>AWS.</b> Athena workgroups, QuickSight and/or Tableau Athena connector, API Gateway + Cognito, ECS PDF renderer, S3 serving-pdf.<br>"
         "<b>Who.</b> Humans via Identity Center + MFA. Apps via Cognito/IAM. render-pdf-role cannot read landing.<br>"
         "<b>Success.</b> Freshness SLO per product; website never lists the raw bucket."),
    ]
    for y, fill, stroke, title, html in blocks:
        style = (
            f"rounded=1;whiteSpace=wrap;html=1;align=left;verticalAlign=top;spacingLeft=16;spacingRight=12;"
            f"spacingTop=10;fontSize=12;fontFamily=Helvetica;fillColor={fill};strokeColor={stroke};strokeWidth=2;"
        )
        p.append(cell(f"b-{y}", f"<b>{title}</b><br><br>{html}", style, 40, y, 1760, 165))
    return "".join(p)


def page3():
    p = []
    p.append(cell("p3t", "Identity, keys, and data zones", TITLE, 40, 16, 900, 36))
    p.append(cell("p3s", "Humans = IAM Identity Center + MFA. Jobs = task roles. CI cannot read landing. KMS is per zone, not per page.", SUB, 40, 52, 1500, 24))
    p.append(cell("p3l", "", LINE, 40, 80, 1800, 8))

    p.append(cell("g-h", "Human access", LANE.format(fill="#FFEBEE", stroke="#DD344C"), 40, 110, 560, 420))
    p.append(icon("h-sso", "g-h", 40, 50, "iam_identity_center", C_SEC, "Identity Center"))
    p.append(icon("h-mfa", "g-h", 200, 50, "cognito", C_SEC, "MFA / app users"))
    p.append(icon("h-lf", "g-h", 360, 50, "lake_formation", C_ANALYTICS, "Lake Formation"))
    p.append(cell("h-n", "Permission sets: analyst (gold), reviewer (artifacts), break-glass (time-bound raw).\nTableau uses a tenant-scoped service role equivalent to analyst — not a personal access key.", NOTE, 20, 200, 520, 180, "g-h"))

    p.append(cell("g-j", "Job identities (ECS / Glue / Lambda)", LANE.format(fill="#FFF3E0", stroke="#E65100"), 640, 110, 560, 420))
    p.append(icon("j-iam", "g-j", 40, 50, "role", C_SEC, "IAM roles"))
    p.append(icon("j-ecs", "g-j", 200, 50, "ecs", C_COMPUTE, "Task role"))
    p.append(icon("j-glue", "g-j", 360, 50, "glue", C_ANALYTICS, "Glue job role"))
    p.append(cell(
        "j-n",
        "ingest: Put landing+inventory\nlayout: Get landing, Textract/Bedrock, Put contracts\nextract: Get landing+contracts, Put silver staging\nmodel: Get silver, Put gold, Update catalog\nrender: Get gold, Put serving-pdf\nCI/CD: Push ECR only",
        NOTE, 20, 180, 520, 200, "g-j",
    ))

    p.append(cell("g-k", "Encryption and network", LANE.format(fill="#E8F5E9", stroke="#2E7D32"), 1240, 110, 560, 420))
    p.append(icon("k-kms", "g-k", 40, 50, "kms", C_SEC, "CMK per zone"))
    p.append(icon("k-vpc", "g-k", 200, 50, "vpc", C_NET, "VPC private"))
    p.append(icon("k-ep", "g-k", 360, 50, "endpoints", C_NET, "Interface/Gateway EP"))
    p.append(cell("k-n", "CMKs: landing, silver, gold, artifacts, logs.\nEnvelope encryption; cache data keys at job/object grain.\nNo public S3. ECR scan on push. Secrets Manager for non-KMS secrets.", NOTE, 20, 200, 520, 180, "g-k"))

    p.append(cell("g-z", "S3 buckets (separate accounts optional; separate CMKs required)", LANE.format(fill="#E3F2FD", stroke="#1565C0"), 40, 560, 1760, 280))
    for i, (res, lab) in enumerate([
        ("s3", "landing"),
        ("s3", "quarantine"),
        ("s3", "bronze"),
        ("s3", "artifacts"),
        ("s3", "silver"),
        ("s3", "gold"),
        ("s3", "serving-pdf"),
        ("s3", "logs/audit"),
    ]):
        p.append(icon(f"bkt{i}", "g-z", 40 + i * 210, 50, res, C_STORAGE, lab))
    p.append(cell("z-n", "Prefix standard: s3://bucket/tenant_id=…/dt=…/document_id=…   Iceberg metadata lives with silver/gold. Quarantine never under a serving prefix.", TXT, 20, 200, 1700, 50, "g-z"))
    return "".join(p)


def page4():
    p = []
    p.append(cell("p4t", "Compute routing and AI boundary", TITLE, 40, 16, 1000, 36))
    p.append(cell("p4s", "Decision is driven by format and size, not by a preferred brand. Glue jobs are the default Spark plane.", SUB, 40, 52, 1500, 24))
    p.append(cell("p4l", "", LINE, 40, 80, 1800, 8))

    p.append(cell("g-r1", "Small / native-text PDF, Word, text", LANE.format(fill="#FFF3E0", stroke="#ED7100"), 40, 110, 420, 360))
    p.append(icon("r1-ecr", "g-r1", 40, 50, "ecr", C_COMPUTE, "ECR image"))
    p.append(icon("r1-ecs", "g-r1", 186, 50, "fargate", C_COMPUTE, "ECS Fargate"))
    p.append(icon("r1-s3", "g-r1", 332, 50, "s3", C_STORAGE, "Silver staging"))
    p.append(cell("r1n", "One task per document or per sheet.\nInterpreter reads contract JSON.\nTimeout/memory bounded.", NOTE, 20, 200, 380, 120, "g-r1"))

    p.append(cell("g-r2", "Scanned or p95–p99 PDF (hundreds–10k pages)", LANE.format(fill="#E0F2F1", stroke="#00796B"), 490, 110, 420, 360))
    p.append(icon("r2-sfn", "g-r2", 40, 50, "step_functions", C_INT, "Map 50 pages"))
    p.append(icon("r2-tx", "g-r2", 186, 50, "textract", C_ML, "Textract async"))
    p.append(icon("r2-red", "g-r2", 332, 50, "lambda", C_COMPUTE, "Reduce / merge"))
    p.append(cell("r2n", "Overlap 1 page for split tables.\nFingerprint each batch; on mismatch start a new contract.\nWatch Textract TPS quota.", NOTE, 20, 200, 380, 120, "g-r2"))

    p.append(cell("g-r3", "Large Excel / CSV", LANE.format(fill="#EDE7F6", stroke="#8C4FFF"), 940, 110, 420, 360))
    p.append(icon("r3-gl", "g-r3", 40, 50, "glue", C_ANALYTICS, "Glue Spark"))
    p.append(icon("r3-emr", "g-r3", 186, 50, "emr", C_ANALYTICS, "EMR if needed"))
    p.append(icon("r3-s3", "g-r3", 332, 50, "s3", C_STORAGE, "Splittable files"))
    p.append(cell("r3n", "Do not OCR workbooks.\nHeader/merged-cell adapter in Spark.\nCompaction of small files in gold.", NOTE, 20, 200, 380, 120, "g-r3"))

    p.append(cell("g-r4", "SQLite snapshot", LANE.format(fill="#F3E5F5", stroke="#6A1B9A"), 1390, 110, 420, 360))
    p.append(icon("r4-ecs", "g-r4", 111, 50, "ecs", C_COMPUTE, "Paged SQL worker"))
    p.append(icon("r4-s3", "g-r4", 257, 50, "s3", C_STORAGE, "Table → Parquet"))
    p.append(cell("r4n", "Integrity + FK checks first.\nOne DB may be one work unit if small;\npage by PK if large. Not a Spark blob.", NOTE, 20, 200, 380, 120, "g-r4"))

    p.append(cell(
        "ai-box",
        "<b>AI boundary</b><br><br>"
        "<b>Allowed:</b> Bedrock/Textract on stratified samples → JSON contract validated against schema → human/CI approval → pin contract_id@version and interpreter image digest.<br><br>"
        "<b>Forbidden in the data plane:</b> model emits Python that is exec’d on landing objects; prompts logged with full page text; per-page Bedrock on a known 10k-page form; model role with s3:PutObject on silver/gold.<br><br>"
        "<b>If generated code is required:</b> pull request → tests → ECR → digest in the contract. Same as any other extractor change.",
        "rounded=1;whiteSpace=wrap;html=1;align=left;verticalAlign=top;spacingLeft=16;spacingTop=12;"
        "fillColor=#FFEBEE;strokeColor=#C62828;strokeWidth=2;fontSize=13;fontFamily=Helvetica;",
        40, 500, 1770, 220,
    ))
    return "".join(p)


def wrap_page(pid, name, width, height, inner):
    return f"""  <diagram id="{pid}" name="{name}">
    <mxGraphModel dx="1400" dy="900" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="{width}" pageHeight="{height}" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
{inner}      </root>
    </mxGraphModel>
  </diagram>
"""


def main():
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<mxfile host="app.diagrams.net" agent="G2i Document Intelligence Lake" version="22.1.16" type="device">\n'
        + wrap_page("medallion", "01 Medallion architecture", 2400, 1400, page1())
        + wrap_page("layers", "02 Layer contracts", 1900, 1400, page2())
        + wrap_page("security", "03 Identity and zones", 1900, 900, page3())
        + wrap_page("compute", "04 Compute and AI", 1900, 780, page4())
        + "</mxfile>\n"
    )
    root = Path(__file__).resolve().parents[2]
    targets = [
        root / "candidate" / "diagrams" / "architecture.drawio",
        root / "internal" / "diagrams" / "architecture.drawio",
    ]
    for t in targets:
        t.write_text(xml, encoding="utf-8")
        print(f"wrote {t} ({len(xml)} bytes)")


if __name__ == "__main__":
    main()
