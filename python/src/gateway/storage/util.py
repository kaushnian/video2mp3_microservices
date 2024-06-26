import pika
import json

import pika.spec


def upload(f, fs, channel, access):
    print('UPLOADING...')
    try:
        # upload file to MongoDB
        fid = fs.put(f)
        print("FID_ID:", fid)
    except Exception as err:
        print(err)
        return "Internal server error", 500

    message = {
        "video_fid": str(fid),
        "mp3_fid": None,
        "username": access["username"],
    }

    try:
        # Put message in queue
        channel.basic_publish(
            # queue default exchange
            exchange="",
            # queue name
            routing_key="video",
            # convert object to json string
            body=json.dumps(message),
            # ensure that messages are persisted in queue in event of restart or crush
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE),
        )
    except Exception as err:
        print(err)
        # Delete file from MongoDB
        fs.delete(fid)
        return "Internal server error", 500
