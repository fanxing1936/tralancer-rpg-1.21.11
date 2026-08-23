# 名牌**下方**那块信息板。实体名牌只渲染一行，换行符不生效，
# 所以另挂一个 text_display 骑在身上。
#
# 三个数都是**现读的属性**，不是写死的 —— 换了武器攻击数字跟着变。
execute if entity @s[scores={rpg_sq_tier=1}] run data modify storage rpg:squad gear set value '皮革'
execute if entity @s[scores={rpg_sq_tier=2}] run data modify storage rpg:squad gear set value '锁链　·　海岸纹饰'
execute if entity @s[scores={rpg_sq_tier=3}] run data modify storage rpg:squad gear set value '铁　·　守护纹饰'
execute if entity @s[scores={rpg_sq_tier=4}] run data modify storage rpg:squad gear set value '钻石　·　沉寂纹饰'
execute if entity @s[scores={rpg_sq_tier=5}] run data modify storage rpg:squad gear set value '下界合金　·　尖塔纹饰'
execute store result storage rpg:squad hp int 1 run attribute @s minecraft:max_health get
execute store result storage rpg:squad ar int 1 run attribute @s minecraft:armor get
execute store result storage rpg:squad atk int 1 run attribute @s minecraft:attack_damage get
function rpg:squad/board_do with storage rpg:squad
