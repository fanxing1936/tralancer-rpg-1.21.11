# 换一身。等级的东西全部重写：数值、甲、纹饰、名牌，外加一把该等的起手剑。
# 手上那把是玩家自己配的，**不动** —— 武器归玩家，甲归等级。
scoreboard players set @s rpg_sq_tier 4
attribute @s minecraft:max_health base set 75
attribute @s minecraft:armor base set 5
attribute @s minecraft:armor_toughness base set 5
attribute @s minecraft:attack_damage base set 5
item replace entity @s armor.head with minecraft:diamond_helmet[minecraft:trim={pattern:"minecraft:silence",material:"minecraft:gold"}]
item replace entity @s armor.chest with minecraft:diamond_chestplate[minecraft:trim={pattern:"minecraft:silence",material:"minecraft:gold"}]
item replace entity @s armor.legs with minecraft:diamond_leggings[minecraft:trim={pattern:"minecraft:silence",material:"minecraft:gold"}]
item replace entity @s armor.feet with minecraft:diamond_boots[minecraft:trim={pattern:"minecraft:silence",material:"minecraft:gold"}]
data modify entity @s CustomName set value [{"text":"佣兵 · ","color":"gray"},{"text":"FABLE","color":"#D9A02B","bold":true}]
scoreboard players set @s rpg_sq_fr 0
tag @s add rpg.sq.fresh
execute at @s run particle happy_villager ~ ~1.6 ~ 0.4 0.5 0.4 0.1 40
execute at @s run particle end_rod ~ ~1 ~ 0.3 0.6 0.3 0.05 24
execute at @s run playsound minecraft:entity.player.levelup player @a[distance=..16] ~ ~ ~ 1 1.2
