# 圣力：每秒 +1，站着不动（祷告）+3，燃着的驱魔图腾 8 格内翻倍，中柱第 2 阶 +15%（按十分之一点累计）
scoreboard players set #r rpg_sef 10
execute if score @s rpg_fz_mv = @s rpg_fz_mv0 run scoreboard players set #r rpg_sef 30
execute if entity @e[type=minecraft:item_display,tag=rpg.totem.lit,distance=..8,limit=1] run scoreboard players operation #r rpg_sef *= #2 rpg_sef
execute if score @s rpg_pillar matches 3 if score @s rpg_sef matches 2.. run function rpg:sephira/force/central
execute if entity @s[tag=rpg.burnt] run scoreboard players set #r rpg_sef 0
scoreboard players operation @s rpg_mana_f += #r rpg_sef
scoreboard players operation #q rpg_sef = @s rpg_mana_f
scoreboard players operation #q rpg_sef /= #10 rpg_sef
scoreboard players operation @s rpg_mana += #q rpg_sef
scoreboard players operation @s rpg_mana_f %= #10 rpg_sef
