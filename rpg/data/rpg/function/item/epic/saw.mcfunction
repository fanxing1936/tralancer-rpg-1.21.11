# 熔锯：60 刻内切六轮，每轮间隔 10 刻 ——
# 生物受伤后约有 10 刻无敌帧，切得更密只是浪费。
execute as @a[tag=rpg.h.dawn_tag1,scores={rpg_saw=50}] at @s run function rpg:item/epic/saw_cut
execute as @a[tag=rpg.h.dawn_tag1,scores={rpg_saw=40}] at @s run function rpg:item/epic/saw_cut
execute as @a[tag=rpg.h.dawn_tag1,scores={rpg_saw=30}] at @s run function rpg:item/epic/saw_cut
execute as @a[tag=rpg.h.dawn_tag1,scores={rpg_saw=20}] at @s run function rpg:item/epic/saw_cut
execute as @a[tag=rpg.h.dawn_tag1,scores={rpg_saw=10}] at @s run function rpg:item/epic/saw_cut
execute as @a[tag=rpg.h.dawn_tag1,scores={rpg_saw=1}] at @s run function rpg:item/epic/saw_cut
execute as @a[tag=rpg.h.dawn_tag1,scores={rpg_saw=1..}] at @s run particle dust_color_transition{from_color:16575098,to_color:8005632,scale:1} ~ ~1 ~ 0.3 0.3 0.3 0.02 3
execute as @a[scores={rpg_saw=1..}] run scoreboard players remove @s rpg_saw 1
