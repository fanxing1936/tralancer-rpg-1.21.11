# 三重热浪：24 / 16 / 8 三个刻各推一圈，半径 3 → 5 → 7。
# 由 rpg:item/epic/epics 守卫调用；不在脉冲刻上时这里只是一次减法。
execute as @a[tag=rpg.h.forge_tag1,scores={rpg_forge=24}] at @s run function rpg:item/epic/forge_ring1
execute as @a[tag=rpg.h.forge_tag1,scores={rpg_forge=16}] at @s run function rpg:item/epic/forge_ring2
execute as @a[tag=rpg.h.forge_tag1,scores={rpg_forge=8}] at @s run function rpg:item/epic/forge_ring3
execute as @a[scores={rpg_forge=1..}] run scoreboard players remove @s rpg_forge 1
