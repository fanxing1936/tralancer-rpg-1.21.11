execute unless score @s rpg_agit matches 100.. run return 0
function rpg:inquest/seal/reindex
execute unless entity @s[tag=rpg.seal.carrier] run return 0
scoreboard players set @s rpg_agit 0
function rpg:inquest/seal/escape
