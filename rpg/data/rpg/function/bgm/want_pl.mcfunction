scoreboard players set @s rpg_bgm_w 2
execute if entity @s[x=0,y=83,z=0,distance=560..] run scoreboard players set @s rpg_bgm_w 3
execute if predicate rpg:paradise/in_fortress run scoreboard players set @s rpg_bgm_w 3
execute if score #moon rpg_pl matches 1.. run scoreboard players set @s rpg_bgm_w 5
execute if entity @s[x=0,y=83,z=0,distance=..36] run scoreboard players set @s rpg_bgm_w 1
execute if score #c1 rpg_pl matches 1..2 if entity @s[x=0,y=83,z=-120,distance=..34] run scoreboard players set @s rpg_bgm_w 4
execute if score #c2 rpg_pl matches 1..2 if entity @s[x=120,y=83,z=0,distance=..34] run scoreboard players set @s rpg_bgm_w 4
execute if score #c3 rpg_pl matches 1..2 if entity @s[x=0,y=83,z=120,distance=..34] run scoreboard players set @s rpg_bgm_w 4
execute if score #c4 rpg_pl matches 1..2 if entity @s[x=-120,y=83,z=0,distance=..34] run scoreboard players set @s rpg_bgm_w 4
