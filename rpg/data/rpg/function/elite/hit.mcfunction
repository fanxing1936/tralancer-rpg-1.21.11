# as 挨打的玩家
tag @s add rpg.el.vic
execute on attacker if entity @s[tag=rpg.el] run function rpg:elite/hit_by
tag @s remove rpg.el.vic
