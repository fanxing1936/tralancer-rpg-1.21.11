# 漩涡的存续。由 rpg:item/extra/skills 守卫调用 ——
# 没人握着利维坦、场上也没有锚时整段跳过。
execute as @e[tag=rpg.levi.anchor] at @s run function rpg:item/extra/leviathan_pull
execute as @e[tag=rpg.levi.anchor] run scoreboard players remove @s rpg_levi_beat 1
execute as @e[tag=rpg.levi.anchor,scores={rpg_levi_beat=..0}] at @s run function rpg:item/extra/leviathan_crush
execute as @e[tag=rpg.levi.anchor,scores={rpg_levi_time=1..}] run scoreboard players remove @s rpg_levi_time 1
execute as @e[tag=rpg.levi.anchor,scores={rpg_levi_time=..0}] at @s run particle splash ~ ~0.4 ~ 1 0.3 1 0.3 40
execute as @e[tag=rpg.levi.anchor,scores={rpg_levi_time=..0}] run kill @s

# 松手即散。trigger 每刻把 hold 顶回 3，这里每刻扣 1 ——
# 只要停手 3 刻，蓄力就清零，没法靠连点攒。
execute as @a[scores={rpg_levi_hold=1..}] run scoreboard players remove @s rpg_levi_hold 1
scoreboard players set @a[scores={rpg_levi_hold=..0,rpg_levi_charge=1..}] rpg_levi_charge 0
