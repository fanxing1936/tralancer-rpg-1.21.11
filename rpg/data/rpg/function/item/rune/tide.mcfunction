# 寒潮［主动］—— 攒满 45 刻后掀起一圈寒潮。
# 守卫在 rpg:item/rune/runes 里，没人握着刻印此石的武器时整段跳过。
execute as @a[tag=rpg.h.tide_tag1,scores={rpg_tide=45..}] at @s run function rpg:item/rune/tide_burst
execute as @a[scores={rpg_tide=1..}] unless entity @s[tag=rpg.h.tide_tag1] run scoreboard players set @s rpg_tide 0
