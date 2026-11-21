execute unless entity @s[tag=rpg.fg.r.bloodpact] run return run attribute @s minecraft:attack_damage modifier remove rpg:forge/bloodpact
execute store result score #hp rpg_fg run data get entity @s Health 100
execute store result score #mx rpg_fg run attribute @s minecraft:max_health get 100
scoreboard players operation #t rpg_fg = #mx rpg_fg
scoreboard players operation #t rpg_fg -= #hp rpg_fg
scoreboard players operation #t rpg_fg *= #10 rpg_fg
scoreboard players operation #t rpg_fg /= #mx rpg_fg
execute if score #t rpg_fg matches 10.. run scoreboard players set #t rpg_fg 9
execute if score #t rpg_fg matches ..-1 run scoreboard players set #t rpg_fg 0
scoreboard players operation #t rpg_fg *= #4 rpg_fg
attribute @s minecraft:attack_damage modifier remove rpg:forge/bloodpact
execute if score #t rpg_fg matches 0 run return 0
execute store result storage rpg:forge bp.p int 1 run scoreboard players get #t rpg_fg
data modify storage rpg:forge bp.z set value ""
execute if score #t rpg_fg matches ..9 run data modify storage rpg:forge bp.z set value "0"
function rpg:forge/rune/bloodpact_set with storage rpg:forge bp
