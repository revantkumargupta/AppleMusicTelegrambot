import os
import time
import telebot
from  gamdl import Gamdl
import traceback
# BOT_TOKEN = os.environ.get('BOT_TOKEN')

bot = telebot.TeleBot('')

@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    # # bot.reply_to(message, message.text)
    # original_message = bot.send_message(message.chat.id, "This message will be edited.")
    # time.sleep(1)
    # bot.send_message(message.chat.id, "This message has been edited.")
    # bot.delete_message(message.chat.id, original_message.message_id)

    if message.text.startswith("https://music.apple.com/"):
        
        dl = Gamdl(
            "l3.wvd",
        "cookies.txt",
            True,
            True,
            "./temp",
            "./",
            False,
            True,
        )
        error_count = 0
        download_queue = []
        for i, url in enumerate([message.text]):
            try:
                download_queue.append(dl.get_download_queue(url.strip()))
            except KeyboardInterrupt:
                exit(1)
            except:
                error_count += 1
                print(f"Failed to check URL {i + 1}/{len(message.text)}")
                bot.reply_to(message, f"Failed to check URL {i + 1}/{len(message.text)}\n{traceback.print_exc()}")
                    
        for i, url in enumerate(download_queue):
            for j, track in enumerate(url):
                track["attributes"]["name"] = track["attributes"]["name"].encode('utf-8').decode('utf-8')
                print(
                    f'Downloading "{track["attributes"]["name"]}" (track {j + 1}/{len(url)} from URL {i + 1}/{len(download_queue)})'
                )
                # print(f"dowwnloading {message.text}")
                bot.reply_to(message, f'Downloading "{track["attributes"]["name"]}" (track {j + 1}/{len(url)} from URL {i + 1}/{len(download_queue)})', parse_mode='HTML')
                track_id = track["id"]
                try:
                    webplayback = dl.get_webplayback(track_id)
                    if track["type"] == "music-videos":
                        tags = dl.get_tags_music_video(
                            track["attributes"]["url"].split("/")[-1].split("?")[0]
                        )
                        final_location = dl.get_final_location(".m4v", tags)
                        if final_location.exists() and not True:
                            continue
                        stream_url_video, stream_url_audio = dl.get_stream_url_music_video(
                            webplayback
                        )
                        decryption_keys_audio = dl.get_decryption_keys_music_video(
                            stream_url_audio, track_id
                        )
                        encrypted_location_audio = dl.get_encrypted_location_audio(track_id)
                        dl.download(encrypted_location_audio, stream_url_audio)
                        decrypted_location_audio = dl.get_decrypted_location_audio(track_id)
                        dl.decrypt(
                            encrypted_location_audio,
                            decrypted_location_audio,
                            decryption_keys_audio,
                        )
                        decryption_keys_video = dl.get_decryption_keys_music_video(
                            stream_url_video, track_id
                        )
                        encrypted_location_video = dl.get_encrypted_location_video(track_id)
                        dl.download(encrypted_location_video, stream_url_video)
                        decrypted_location_video = dl.get_decrypted_location_video(track_id)
                        dl.decrypt(
                            encrypted_location_video,
                            decrypted_location_video,
                            decryption_keys_video,
                        )
                        fixed_location = dl.get_fixed_location(track_id, ".m4v")
                        dl.fixup_music_video(
                            decrypted_location_audio,
                            decrypted_location_video,
                            fixed_location,
                        )
                        final_location.parent.mkdir(parents=True, exist_ok=True)
                        dl.move_final(final_location, fixed_location, tags)
                    else:
                        unsynced_lyrics, synced_lyrics = dl.get_lyrics(track_id)
                        tags = dl.get_tags_song(webplayback, unsynced_lyrics)
                        final_location = dl.get_final_location(".m4a", tags)
                        if False:
                            final_location.parent.mkdir(parents=True, exist_ok=True)
                            dl.make_lrc(final_location, synced_lyrics)
                            continue
                        if final_location.exists() and not True:
                            continue
                        stream_url = dl.get_stream_url_song(webplayback)
                        decryption_keys = dl.get_decryption_keys_song(stream_url, track_id)
                        encrypted_location = dl.get_encrypted_location_audio(track_id)
                        dl.download(encrypted_location, stream_url)
                        decrypted_location = dl.get_decrypted_location_audio(track_id)
                        dl.decrypt(encrypted_location, decrypted_location, decryption_keys)
                        fixed_location = dl.get_fixed_location(track_id, ".m4a")
                        dl.fixup_song(decrypted_location, fixed_location)
                        final_location.parent.mkdir(parents=True, exist_ok=True)
                        dl.move_final(final_location, fixed_location, tags)
                        if not False:
                            dl.make_lrc(final_location, synced_lyrics)
                        # bot.send_message(replied.chat.id, f"Downloaded {final_location}")
                        # bot.delete_message(message.chat.id, replied.message_id)
                        if os.path.exists(final_location):
                            with open(final_location, 'rb') as f:
                                bot.send_document(message.chat.id, f)
                            os.remove(final_location)
                except KeyboardInterrupt:
                    exit(1)
                except:
                    error_count += 1
                    print(f"failed to download {message.text}")
                    # print(
                    #     f'Failed to download "{track["attributes"]["name"]}" (track {j + 1}/{len(url)} from URL {i + 1}/{len(download_queue)})'
                    # )
                    bot.reply_to(message, f"{traceback.print_exc()}")
                dl.cleanup()
    else:
        bot.reply_to(message, "URL must start with https://music.apple.com/")
    print(f"Done ({error_count} error(s))")
    


bot.infinity_polling()
