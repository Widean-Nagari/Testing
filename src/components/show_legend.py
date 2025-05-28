import streamlit as st
import streamlit.components.v1 as components
import base64

def show():
    attendant = get_base64_image("src/public/attendant.png")
    male = get_base64_image("src/public/male.png")
    female = get_base64_image("src/public/female.png")
    donotmove = get_base64_image("src/public/donotmove.png")
    vip = get_base64_image("src/public/vip.png")
    loyalty = get_base64_image("src/public/loyalty.png")
    share = get_base64_image("src/public/share.png")
    indirect = get_base64_image("src/public/indirect.png")
    clean = get_base64_image("src/public/clean.png")
    dirty = get_base64_image("src/public/dirty.png")
    inspect = get_base64_image("src/public/inspect.png")
    pickup = get_base64_image("src/public/pickup.png")
    turndown = get_base64_image("src/public/turndown.png")
    components.html(f"""
    <style>
        .legend {{
            color: white;
            display: flex;
            align-items: center;
            flex-wrap: wrap;
            font-family: Arial, sans-serif;
            font-size: 14px;
        }}
        .legend-item {{
            display: flex;
            align-items: center;
            margin: 5px 10px;
        }}

        .color-box {{
            width: 32px;
            height: 32px;
            display: inline-block;
            margin-right: 5px;
        }}

        .icon-placeholder {{
            width: 32px;
            height: 32px;
            display: inline-block;
            margin-right: 5px;
            background-size: contain;
            background-repeat: no-repeat;
        }}

        /* Define colors (same as image) */
        .in-house {{ background-color: #77c043; }}
        .reserved {{ background-color: #f8a44c; }}
        .pre-registered {{ background-color: #e74857; }}
        .out-of-order {{ background-color: #ccc; }}
        .room-hold {{ background-color: #30bfbf; }}
        .lease {{ background-color: #d692e0; }}
        .not-in-inventory {{ background-color: #111; }}
        .occupied {{ background-color: #c1dc42; }}

        /* Placeholder URLs for icons */
        .attendant-icon {{ background-image: url('data:image/png;base64,{attendant}'); }}
        .male-icon {{ background-image: url('data:image/png;base64,{male}'); }}
        .female-icon {{ background-image: url('data:image/png;base64,{female}'); }}
        .do-not-move-icon {{ background-image: url('data:image/png;base64,{donotmove}'); }}
        .vip-icon {{ background-image: url('data:image/png;base64,{vip}'); }}
        .loyalty-icon {{ background-image: url('data:image/png;base64,{loyalty}'); }}
        .share-icon {{ background-image: url('data:image/png;base64,{share}'); }}
        .indirect-icon {{ background-image: url('data:image/png;base64,{indirect}'); }}
        .clean-icon {{ background-image: url('data:image/png;base64,{clean}'); }}
        .dirty-icon {{ background-image: url('data:image/png;base64,{dirty}'); }}
        .inspect-icon {{ background-image: url('data:image/png;base64,{inspect}'); }}
        .pickup-icon {{ background-image: url('data:image/png;base64,{pickup}'); }}
        .turn-down-icon {{ background-image: url('data:image/png;base64,{turndown}'); }}
    </style>
    <div class="legend">
        <div class="legend-item">
            <span class="color-box in-house"></span> In House
        </div>
        <div class="legend-item">
            <span class="color-box reserved"></span> Reserved
        </div>
        <div class="legend-item">
            <span class="color-box pre-registered"></span> Pre-registered
        </div>
        <div class="legend-item">
            <span class="color-box out-of-order"></span> Out Of Order
        </div>
        <div class="legend-item">
            <span class="color-box room-hold"></span> Room Hold
        </div>
        <div class="legend-item">
            <span class="color-box lease"></span> Lease
        </div>
        <div class="legend-item">
            <span class="color-box not-in-inventory"></span> Not in Inventory
        </div>
        <div class="legend-item">
            <span class="icon-placeholder attendant-icon"></span> Attendant in Room
        </div>
        <div class="legend-item">
            <span class="icon-placeholder male-icon"></span> Male
        </div>
        <div class="legend-item">
            <span class="icon-placeholder female-icon"></span> Female
        </div>
        <div class="legend-item">
            <span class="icon-placeholder do-not-move-icon"></span> Do Not Move
        </div>
        <div class="legend-item">
            <span class="icon-placeholder vip-icon"></span> VIP
        </div>
        <div class="legend-item">
            <span class="icon-placeholder loyalty-icon"></span> Loyalty Member
        </div>
        <div class="legend-item">
            <span class="icon-placeholder share-icon"></span> Share
        </div>
        <div class="legend-item">
            <span class="icon-placeholder indirect-icon"></span> Indirect
        </div>
        <div class="legend-item">
            <span class="icon-placeholder clean-icon"></span> Clean
        </div>
        <div class="legend-item">
            <span class="icon-placeholder dirty-icon"></span> Dirty
        </div>
        <div class="legend-item">
            <span class="icon-placeholder inspect-icon"></span> Inspect
        </div>
        <div class="legend-item">
            <span class="icon-placeholder pickup-icon"></span> Pickup
        </div>
        <div class="legend-item">
            <span class="icon-placeholder turn-down-icon"></span> Turn Down
        </div>
    </div>
    """, height=200)

def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        base64_bytes = base64.b64encode(img_file.read()).decode("utf-8")
    return base64_bytes
