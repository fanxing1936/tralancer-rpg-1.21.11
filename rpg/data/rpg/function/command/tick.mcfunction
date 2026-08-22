function rpg:item/chestplate/off


function rpg:item/sword/off/off

function rpg:item/bow/off


function rpg:item/sword/main/sweep/sweep_trigger
function rpg:item/sword/main/sweep/sweep_into

function rpg:item/sword/main/flame/flame_into
function rpg:item/sword/main/flame/flame_trigger

function rpg:item/sword/main/wind/wind_into
function rpg:item/sword/main/wind/wind_trigger

function rpg:item/bow/legend/bubble/bubble
function rpg:item/bow/legend/burn/burn
function rpg:item/bow/legend/hunter/hunter

function rpg:item/extra/skills




function rpg:command/com




function rpg:task/trial/trial

function rpg:loot/loot

function rpg:level/player


#生物检测

execute if entity @e[type=#minecraft:skeletons,tag=!skeleton,limit=1] run function rpg:command/spawn/skeleton_batch


execute if entity @e[type=#minecraft:zombies,tag=!zombie,limit=1] run function rpg:command/spawn/zombie_batch

execute if entity @e[type=minecraft:creeper,tag=!creeper,limit=1] run function rpg:command/spawn/creeper_batch

