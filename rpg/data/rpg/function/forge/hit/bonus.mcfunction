scoreboard players operation #bd rpg_fg = #d rpg_fg
scoreboard players operation #bd rpg_fg *= #pct rpg_fg
scoreboard players operation #bd rpg_fg /= #100 rpg_fg
execute if score #bd rpg_fg matches ..0 run scoreboard players set #bd rpg_fg 1
execute store result storage rpg:forge dmg.n int 1 run scoreboard players get #bd rpg_fg
function rpg:forge/hit/dmg with storage rpg:forge dmg
particle minecraft:crit ~ ~1 ~ 0.3 0.4 0.3 0.2 6
