# #v rpg_fg（×100 的整数）-> storage rpg:forge ui.<f.key>，两位小数，补零。
scoreboard players operation #fi rpg_fg = #v rpg_fg
scoreboard players operation #fi rpg_fg /= #100 rpg_fg
scoreboard players operation #ff rpg_fg = #v rpg_fg
scoreboard players operation #ff rpg_fg %= #100 rpg_fg
execute store result storage rpg:forge f.i int 1 run scoreboard players get #fi rpg_fg
execute store result storage rpg:forge f.d int 1 run scoreboard players get #ff rpg_fg
data modify storage rpg:forge f.z set value ""
execute if score #ff rpg_fg matches ..9 run data modify storage rpg:forge f.z set value "0"
function rpg:forge/fmt_set with storage rpg:forge f
