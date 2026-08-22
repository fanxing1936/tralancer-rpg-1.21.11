# 逆潮［被动］—— 生命跌破三成时回涌一次，之后要等 30 秒才会再涌。
# 血量直接读 damage_action：rpg:command/index 每刻已经抓好，零额外开销。
execute as @a[tag=rpg.h.ebb_tag1,scores={rpg_rune_ebb=1..}] run scoreboard players remove @s rpg_rune_ebb 1
execute as @a[tag=rpg.h.ebb_tag1,scores={rpg_rune_ebb=..0,damage_action=..5}] at @s run function rpg:item/rune/ebb_surge
