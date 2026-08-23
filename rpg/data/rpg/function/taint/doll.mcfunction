# 人偶替你脏。这一轮沾上多少，就从你身上还回去多少，转嫁到它身上。
#
# #t1 是上一步算出来的"这一轮的净增量"，所以扣得精确 ——
# 不用去猜玩家手里握着几件魔器。
scoreboard players operation @s rpg_taint -= #t1 rpg_hud
function rpg:hud/m16
execute as @e[type=minecraft:allay,tag=rpg.doll,distance=..16,limit=1,sort=nearest] at @s run function rpg:doll/hurt
