import os
import uuid
import qrcode

SESSION_FOLDER = "sessions"

os.makedirs(SESSION_FOLDER, exist_ok=True)


class PairService:

    def generate_qr(self):
        session_id = str(uuid.uuid4())[:8]

        qr_data = f"SpaceXBot-{session_id}"

        filename = f"{session_id}.png"

        filepath = os.path.join(SESSION_FOLDER, filename)

        img = qrcode.make(qr_data)

        img.save(filepath)

        return {
            "session_id": session_id,
            "qr_image": filename
        }


pair_service = PairService()
