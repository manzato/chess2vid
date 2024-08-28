
all: run



run: 
	poetry run chess2vid -i '/home/manzato/projects/chess2vid/manzato_vs_jakubhromek_2023.12.23.pgn' --frame-width=240 --frame-height=180 --blender-bin "/home/manzato/projects/tools/blender-4.0.2-linux-x64/blender"
#	poetry run chess2vid -i '/home/manzato/projects/chess2vid/manzato_vs_jakubhromek_2023.12.23.pgn' --blender-bin "/home/manzato/projects/tools/blender-4.0.2-linux-x64/blender"

