execute store result score #n rpg_jq if entity @e[tag=rpg.jqb.guard]
execute if score #n rpg_jq matches 4.. run return run function rpg:jacques_boss/skill/volley
function rpg:jacques_boss/skill/horn
