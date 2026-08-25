
# 即时射线始终保留 @s=施术玩家，伤害来源明确为 by @s。
scoreboard players set @s sweep 0
playsound minecraft:entity.player.attack.crit player @s ~ ~ ~ 1 1
execute anchored eyes positioned ^ ^ ^1 run function rpg:item/legacy_advanced/rune/sweep_ray_1
function rpg:hud/m20
