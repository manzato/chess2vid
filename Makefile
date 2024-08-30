
all: run



run: 
	poetry run chess2vid -i '/home/manzato/projects/chess2vid/resources/games/short.pgn' --frame-width=480 --frame-height=240 --blender-bin "/home/manzato/projects/tools/blender-4.0.2-linux-x64/blender" --save-blender short.blend -o ./short_frames -r 1:1
	#poetry run chess2vid -i '/home/manzato/projects/chess2vid/resources/games/short.pgn' --frame-width=120 --frame-height=90 --blender-bin "/home/manzato/projects/tools/blender-4.0.2-linux-x64/blender" --save-blender short.blend -o ./short_frames -r 1:4
	#poetry run chess2vid -i '/home/manzato/projects/chess2vid/resources/games/manzato_vs_jakubhromek_2023.12.23.pgn' --blender-bin "/home/manzato/projects/tools/blender-4.0.2-linux-x64/blender"

