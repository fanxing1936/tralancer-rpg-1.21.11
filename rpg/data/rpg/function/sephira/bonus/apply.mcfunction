# 按当前阶位和主柱重挂全部修饰符（晋阶、选柱、迁移时调）
attribute @s minecraft:max_health modifier remove rpg:sephira
attribute @s minecraft:attack_damage modifier remove rpg:sef_dmg
attribute @s minecraft:attack_speed modifier remove rpg:sef_spd
attribute @s minecraft:armor modifier remove rpg:sef_arm
execute if score @s rpg_sef matches 2 run attribute @s minecraft:max_health modifier add rpg:sephira 4 add_value
execute if score @s rpg_sef matches 3 run attribute @s minecraft:max_health modifier add rpg:sephira 8 add_value
execute if score @s rpg_sef matches 4 run attribute @s minecraft:max_health modifier add rpg:sephira 12 add_value
execute if score @s rpg_sef matches 5 run attribute @s minecraft:max_health modifier add rpg:sephira 16 add_value
execute if score @s rpg_sef matches 6 run attribute @s minecraft:max_health modifier add rpg:sephira 20 add_value
execute if score @s rpg_sef matches 7 run attribute @s minecraft:max_health modifier add rpg:sephira 24 add_value
execute if score @s rpg_sef matches 8 run attribute @s minecraft:max_health modifier add rpg:sephira 28 add_value
execute if score @s rpg_sef matches 9 run attribute @s minecraft:max_health modifier add rpg:sephira 32 add_value
execute if score @s rpg_sef matches 10 run attribute @s minecraft:max_health modifier add rpg:sephira 36 add_value
# 严厉柱：第 3、6 阶伤害各 +5%，第 8 阶攻速 +10%
execute if score @s rpg_pillar matches 1 if score @s rpg_sef matches 3..5 run attribute @s minecraft:attack_damage modifier add rpg:sef_dmg 0.05 add_multiplied_base
execute if score @s rpg_pillar matches 1 if score @s rpg_sef matches 6.. run attribute @s minecraft:attack_damage modifier add rpg:sef_dmg 0.10 add_multiplied_base
execute if score @s rpg_pillar matches 1 if score @s rpg_sef matches 8.. run attribute @s minecraft:attack_speed modifier add rpg:sef_spd 0.10 add_multiplied_base
# 慈悲柱：第 4、7 阶护甲各 +2
execute if score @s rpg_pillar matches 2 if score @s rpg_sef matches 4..6 run attribute @s minecraft:armor modifier add rpg:sef_arm 2 add_value
execute if score @s rpg_pillar matches 2 if score @s rpg_sef matches 7.. run attribute @s minecraft:armor modifier add rpg:sef_arm 4 add_value
# 力条上限：100，第 4、7、9 阶各 +20，中柱第 10 阶再 +40
scoreboard players set @s rpg_mana_max 100
execute if score @s rpg_sef matches 4.. run scoreboard players add @s rpg_mana_max 20
execute if score @s rpg_sef matches 7.. run scoreboard players add @s rpg_mana_max 20
execute if score @s rpg_sef matches 9.. run scoreboard players add @s rpg_mana_max 20
execute if score @s rpg_pillar matches 3 if score @s rpg_sef matches 10 run scoreboard players add @s rpg_mana_max 40
function rpg:paths/bless/apply
