scoreboard players set #xa rpg_fg 100
function rpg:forge/xp/add
item modify entity @s weapon.mainhand {function:"minecraft:set_count",count:-1,add:true}
function rpg:forge/ui/done
execute if score #up rpg_fg matches 1.. run function rpg:forge/xp/up
