advancement revoke @s only rpg:pvp/safe
execute unless entity @s[tag=rpg.safe] run return 0
function rpg:pvp/undo
title @s actionbar ["",{"text":"镇里和营地里不能动手","color":"#797979","bold":false,"italic":false}]
