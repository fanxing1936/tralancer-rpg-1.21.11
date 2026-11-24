# 对话框传回的昵称（宏 n）。只认流程里、停在这一步的人
execute unless score @s rpg_ob matches 2 run return 0
playsound minecraft:block.note_block.chime master @s ~ ~ ~ 0.55 1.2
$data modify storage rpg:onboard tmp.n set value "$(n)"
execute if data storage rpg:onboard tmp{n:""} run return run function rpg:onboard/name/retry
function rpg:onboard/name/keep
