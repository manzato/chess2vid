#ffmpeg -y -start_number 1 -i %d.png -c:v libx264 -r 24.97 -pix_fmt yuv420p output.mp4
ffmpeg -y -start_number 1 -i %d.png -c:v libx265 output.mp4
