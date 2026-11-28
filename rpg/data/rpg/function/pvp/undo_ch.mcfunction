advancement revoke @s only rpg:pvp/ch
execute unless entity @s[tag=rpg.ch] run return 0
function rpg:pvp/undo
title @s actionbar ["",{"text":"同阵营不伤友军","color":"#797979","bold":false,"italic":false}]
