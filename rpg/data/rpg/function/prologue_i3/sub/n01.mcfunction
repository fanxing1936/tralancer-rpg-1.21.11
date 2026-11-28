bossbar set rpg:prologue_zh_i3 name [{"translate":"rpg.prologue.N01.zh","fallback":"起初，神造天地，又造众天使侍立在宝座前。","color":"#BFB8A8","italic":false}]
bossbar set rpg:prologue_en_i3 name [{"translate":"rpg.prologue.N01.en","fallback":"In the beginning God created the heaven and the","color":"#BFB8A8","italic":true}]
scoreboard players set #sub rpg_pr_i3 124
scoreboard players set #subn rpg_pr_i3 101
execute as @a[tag=rpg.pri3] at @s run playsound rpg:vo.prologue.n01 voice @s ~ ~ ~ 1 1
