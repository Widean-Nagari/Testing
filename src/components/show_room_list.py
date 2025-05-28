import streamlit as st
import streamlit.components.v1 as components
import datetime

def show(start_date, height=600):
    day_count = 7
    st.write(f"Room information and calendar for the next {day_count} days.")
    dates = [(start_date + datetime.timedelta(days=i)).strftime("%a %d") for i in range(day_count)]
    current_date = start_date.strftime("%b %Y")

    rooms = [
        ["101", "Single", "1st Floor", "Sea View", "Balcony, King Bed", "No", "Yes"],
        ["102", "Double", "2nd Floor", "Mountain View", "Twin Beds, Fireplace", "Yes", "No"],
        ["103", "Suite", "3rd Floor", "City View", "Jacuzzi, King Bed", "No", "Yes"],
        ["104", "Deluxe", "4th Floor", "Garden View", "Balcony, Queen Bed", "No", "Yes"],
        ["105", "Presidential", "5th Floor", "Ocean View", "Private Pool, King Bed", "No", "Yes"]
    ]

    reservations = [
        ["101", "2025-05-29", "2025-05-31", "John Doe", "RES-123456", "2/0", "0 IDR", "INTA", "0 IDR", "100", "AGODA"],
        ["104", "2025-05-30", "2025-06-02", "Jane Doe", "RES-654321", "2/0", "0 IDR", "INTA", "0 IDR", "100", "DIRECT"],
    ]

    valid_reservations = []
    for r in reservations:
        start_date_str = start_date.strftime("%Y-%m-%d")
        end_date_str = (start_date + datetime.timedelta(days=day_count - 1)).strftime("%Y-%m-%d")
        if start_date_str <= r[1] <= end_date_str and start_date_str <= r[2] <= end_date_str:
            valid_reservations.append(r)
        elif r[1] < start_date_str and r[2] > end_date_str:
            r[1] = start_date_str
            r[2] = end_date_str
            valid_reservations.append(r)
        elif r[1] < start_date_str and start_date_str <= r[2] <= end_date_str:
            r[1] = start_date_str
            valid_reservations.append(r)
        elif r[2] > end_date_str and start_date_str <= r[1] <= end_date_str:
            r[2] = end_date_str
            valid_reservations.append(r)

    for reservation in valid_reservations:
        reservation[1] = datetime.datetime.strptime(reservation[1], "%Y-%m-%d").strftime("%a %d")
        reservation[2] = datetime.datetime.strptime(reservation[2], "%Y-%m-%d").strftime("%a %d")

    rows = "".join([
        f"<tr>"
        f"<td onmouseenter=\"showModal('Room Properties', 'Room Number: {room[0]}<br>Room Type: {room[1]}<br>Floor: {room[2]}<br>Exposure: {room[3]}<br>Attributes: {room[4]}<br>Smoking: {room[5]}<br>Clean: {room[6]}')\" onmouseleave=\"closeModal()\">{room[0]}</td>"
        f"<td onmouseenter=\"showModal('Room Properties', 'Room Number: {room[0]}<br>Room Type: {room[1]}<br>Floor: {room[2]}<br>Exposure: {room[3]}<br>Attributes: {room[4]}<br>Smoking: {room[5]}<br>Clean: {room[6]}')\" onmouseleave=\"closeModal()\">{room[1]}</td>"
        + "".join([
            f"<td>"
            f"<div style=\"display: flex;\">"
            f"{''.join([
                f'<div onmouseenter=\"showModal(\'{reservation[0]} - {reservation[3]}\', \'Confirmation Number: {reservation[4]}<br>Arrival Date: {reservation[1]}<br>Departure Date: {reservation[2]}<br>Adult: {reservation[5]}<br>Rate: {reservation[6]}<br>Rate Plan: {reservation[7]}<br>Folio Balance: {reservation[8]}<br>Settlement Type: {reservation[9]}<br>Booking Agency: {reservation[10]}\')\" onmouseleave=\"closeModal()\" class=\"reservation-card\" draggable=\"true\">{reservation[3]}<div class="resizer left"></div><div class="resizer right"></div></div>'
                for reservation in valid_reservations
                    if reservation[0] == room[0] and
                    dates.index(reservation[1]) <= i <= dates.index(reservation[2])
                ])
            }"
            f"</div>"
            f"</td>"
            for i in range(day_count)
        ]) +
        "</tr>"
        for room in rooms
    ])

    components.html(f"""
    <div id=\"room-details-modal\" style=\"
        display: none;
        position: fixed;
        top: 10%;
        left: 50%;
        transform: translate(-50%, -20%);
        background-color: white;
        border: 1px solid #ddd;
        padding: 0 20px;
        z-index: 1000;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
        font-family: Arial, sans-serif;
        overflow: auto;
    ">
        <h3 id="room-details-title"></h3>
        <p id=\"room-details-content\"></p>
    </div>
    <table border=\"1\" style=\"width: 100%; font-family: Arial, sans-serif; color: white;\">
        <tr>
            <th rowspan=\"2\">Room</th>
            <th rowspan=\"2\">Room Type</th>
            <th colspan={day_count}>{current_date}</th>
        </tr>
        <tr>
            {''.join([f'<th>{date}</th>' for date in dates])}
        </tr>
        {rows}
    </table>

    <style>
        .reservation-card {{
            background-color: #4CAF50;
            color: white;
            text-align: center;
            padding: 5px;
            border-radius: 5px;
            margin: 2px;
            font-size: 12px;
            position: absolute;
            transform: translateY(-15px);
            cursor: move;
        }}
        .resizer {{
            width: 10px;
            height: 100%;
            cursor: ew-resize;
            position: absolute;
            top: 0;
        }}
        .resizer.left {{
            left: -5px; /* Half width of resizer to center */
        }}
        .resizer.right {{
            right: -5px; /* Half width of resizer to center */
        }}
    </style>
    <script>
        function showModal(title, details) {{
            const modal = document.getElementById('room-details-modal');
            const modalTitle = document.getElementById('room-details-title');
            const content = document.getElementById('room-details-content');
            modalTitle.innerHTML = title;
            content.innerHTML = details;
            modal.style.display = 'block';
        }}

        function closeModal() {{
            const modal = document.getElementById('room-details-modal');
            modal.style.display = 'none';
        }}

        const cards = document.querySelectorAll('.reservation-card');
        let draggedCard = null;
        let isResizing = false;
        let currentResizer = null;
        cards.forEach(card => {{
            card.addEventListener('dragstart', (event) => {{
                draggedCard = card; // Store reference to the dragged card
                card.style.opacity = '0.5'; // Change appearance while dragging
            }});

            card.addEventListener('dragend', () => {{
                card.style.opacity = ''; // Restore appearance when dragging ends
            }});
        }});

        document.addEventListener('dragover', (event) => {{
            event.preventDefault(); // Prevent default to allow drop
        }});

        document.addEventListener('drop', (event) => {{
            event.preventDefault(); // Prevent default action

            // Get the drop location
            const x = event.clientX;
            const y = event.clientY;

            // Move the dragged card to the drop location
            if (draggedCard) {{
                draggedCard.style.left = (x - draggedCard.offsetWidth / 2) + 'px'; // Center the card on drop
                draggedCard.style.top = (y - draggedCard.offsetHeight / 2) + 'px'; // Center the card on drop
            }}
        }});

        // Resizing functionality
        document.querySelectorAll('.resizer').forEach(resizer => {{
            resizer.addEventListener('mousedown', (event) => {{
                isResizing = true;
                currentResizer = resizer.parentNode;
            }});
        }});

        document.addEventListener('mousemove', (event) => {{
            if (isResizing && currentResizer) {{
                const width = event.clientX - currentResizer.getBoundingClientRect().left;
                if (width > 50) {{ // Minimum width
                    currentResizer.style.width = width + 'px';
                }}
            }}
        }});

        document.addEventListener('mouseup', () => {{
            isResizing = false;
            currentResizer = null;
        }});
    </script>
    """, height=height, scrolling=True)
