# 视角被扯一下。rotate 的角度只能是字面量，所以掷完点走一条宏。
execute store result storage rpg:fall yaw int 1 run random value -80..80
execute store result storage rpg:fall pit int 1 run random value -25..25
function rpg:taint/yank with storage rpg:fall
