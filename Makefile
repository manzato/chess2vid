
all: short

BLENDER="/home/manzato/projects/tools/blender-4.0.2-linux-x64/blender"



real:
	poetry run chess2vid -i './resources/games/manzato_vs_jakubhromek_2023.12.23.pgn' --frame-width=1024 --frame-height=768 --blender-bin ${BLENDER} --save-blender real.blend -o ./real_frames -r 200:210 --verbose


short: 
	poetry run chess2vid -i './resources/games/short.pgn' --frame-width=480 --frame-height=240 --blender-bin ${BLENDER} --save-blender short.blend -o ./short_frames -r 1:1

scholar:
	poetry run chess2vid -i './resources/games/scholar.pgn' --blender-bin ${BLENDER} -o ./scholar_frames -r 1: