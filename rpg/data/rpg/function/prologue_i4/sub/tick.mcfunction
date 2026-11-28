execute unless score #sub rpg_pr_i4 matches 1.. run return 0
scoreboard players remove #sub rpg_pr_i4 1
execute if score #subn rpg_pr_i4 matches 101 if score #sub rpg_pr_i4 matches 62 run bossbar set rpg:prologue_en_i4 name [{"translate":"rpg.prologue.N01.en_2","fallback":"earth, and the angels to stand before His throne.","color":"#BFB8A8","italic":true}]
execute if score #subn rpg_pr_i4 matches 102 if score #sub rpg_pr_i4 matches 129 run bossbar set rpg:prologue_en_i4 name [{"translate":"rpg.prologue.N02.en_2","fallback":"Lucifer, the son of the morning. God gave him both","color":"#BFB8A8","italic":true}]
execute if score #subn rpg_pr_i4 matches 102 if score #sub rpg_pr_i4 matches 65 run bossbar set rpg:prologue_en_i4 name [{"translate":"rpg.prologue.N02.en_3","fallback":"Authority and Might, and set him above all the angels.","color":"#BFB8A8","italic":true}]
execute if score #subn rpg_pr_i4 matches 104 if score #sub rpg_pr_i4 matches 62 run bossbar set rpg:prologue_en_i4 name [{"translate":"rpg.prologue.N04.en_2","fallback":"heaven, I will exalt my throne above the stars of God.","color":"#BFB8A8","italic":true}]
execute if score #subn rpg_pr_i4 matches 105 if score #sub rpg_pr_i4 matches 41 run bossbar set rpg:prologue_en_i4 name [{"translate":"rpg.prologue.N05.en_2","fallback":"called in the Hebrew tongue Armageddon.","color":"#BFB8A8","italic":true}]
execute if score #subn rpg_pr_i4 matches 106 if score #sub rpg_pr_i4 matches 80 run bossbar set rpg:prologue_en_i4 name [{"translate":"rpg.prologue.N06.en_2","fallback":"his Authority. It became a thread of green smoke and fled into the closing rift.","color":"#BFB8A8","italic":true}]
execute if score #subn rpg_pr_i4 matches 107 if score #sub rpg_pr_i4 matches 61 run bossbar set rpg:prologue_en_i4 name [{"translate":"rpg.prologue.N07.en_2","fallback":"it, passed to the one who stands against God.","color":"#BFB8A8","italic":true}]
execute if score #subn rpg_pr_i4 matches 206 if score #sub rpg_pr_i4 matches 63 run bossbar set rpg:prologue_en_i4 name [{"translate":"rpg.prologue.T06.en_2","fallback":"four of the Throne's eye-wheels within 3 seconds","color":"#D8D2C4","italic":false}]
execute if score #sub rpg_pr_i4 matches 0 run bossbar set rpg:prologue_zh_i4 name ""
execute if score #sub rpg_pr_i4 matches 0 run bossbar set rpg:prologue_en_i4 name ""
