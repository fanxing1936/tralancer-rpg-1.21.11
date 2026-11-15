# 权柄线（as/at 圣卫）：从他胸前拉到这名圣卫
scoreboard players operation #id rpg_ub = @s rpg_ub_id
execute at @e[type=minecraft:vindicator,tag=rpg.usb,limit=1,sort=nearest] positioned ~ ~1.6 ~ facing entity @s eyes run function rpg:usurper_boss/auth/beam
