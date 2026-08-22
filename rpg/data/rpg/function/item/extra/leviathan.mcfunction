# 漩涡的存续。由 rpg:item/extra/skills 守卫调用 ——
# 没人握着利维坦、场上也没有锚时整段跳过。
execute as @e[tag=rpg.levi.anchor] at @s run function rpg:item/extra/leviathan_pull
execute as @e[tag=rpg.levi.anchor] run scoreboard players remove @s rpg_levi_beat 1
execute as @e[tag=rpg.levi.anchor,scores={rpg_levi_beat=..0}] at @s run function rpg:item/extra/leviathan_crush
execute as @e[tag=rpg.levi.anchor,scores={rpg_levi_time=1..}] run scoreboard players remove @s rpg_levi_time 1
execute as @e[tag=rpg.levi.anchor,scores={rpg_levi_time=..0}] at @s run particle splash ~ ~0.4 ~ 1 0.3 1 0.3 40
execute as @e[tag=rpg.levi.anchor,scores={rpg_levi_time=..0}] run kill @s
