bossbar set rpg:prologue_zh_i4 name [{"translate":"rpg.prologue.who.belial.zh","fallback":"贝利尔","color":"#D97AD9","italic":false,"bold":true},{"text":"：","color":"#D97AD9","bold":true},{"translate":"rpg.prologue.D04.zh","fallback":"赢了以后，天上归谁？","color":"#FFFFFF","italic":false}]
bossbar set rpg:prologue_en_i4 name [{"translate":"rpg.prologue.who.belial.en","fallback":"Belial","color":"#D97AD9","italic":false,"bold":true},{"text":": ","color":"#D97AD9","bold":true},{"translate":"rpg.prologue.D04.en","fallback":"And when we've won — whose is Heaven?","color":"#D8D2C4","italic":false}]
scoreboard players set #sub rpg_pr_i4 61
scoreboard players set #subn rpg_pr_i4 304
execute as @a[tag=rpg.pri4] at @s run playsound rpg:vo.prologue.d04 voice @s ~ ~ ~ 1 1
