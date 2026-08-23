# 换一身。等级的东西全部重写：数值、甲、纹饰、名牌，外加一把该等的起手剑。
# 手上那把是玩家自己配的，**不动** —— 武器归玩家，甲归等级。
scoreboard players set @s rpg_sq_tier 3
attribute @s minecraft:max_health base set 55
attribute @s minecraft:armor base set 5
attribute @s minecraft:armor_toughness base set 2
attribute @s minecraft:attack_damage base set 3
item replace entity @s armor.head with minecraft:iron_helmet[minecraft:trim={pattern:"minecraft:ward",material:"minecraft:iron"}]
item replace entity @s armor.chest with minecraft:iron_chestplate[minecraft:trim={pattern:"minecraft:ward",material:"minecraft:iron"}]
item replace entity @s armor.legs with minecraft:iron_leggings[minecraft:trim={pattern:"minecraft:ward",material:"minecraft:iron"}]
item replace entity @s armor.feet with minecraft:iron_boots[minecraft:trim={pattern:"minecraft:ward",material:"minecraft:iron"}]
data modify entity @s CustomName set value [{"text":"佣兵 · ","color":"gray"},{"text":"OPUS","color":"#A275DE","bold":true}]
scoreboard players set @s rpg_sq_fr 0
tag @s add rpg.sq.fresh
execute at @s run particle happy_villager ~ ~1.6 ~ 0.4 0.5 0.4 0.1 40
execute at @s run particle end_rod ~ ~1 ~ 0.3 0.6 0.3 0.05 24
execute at @s run playsound minecraft:entity.player.levelup player @a[distance=..16] ~ ~ ~ 1 1.2
