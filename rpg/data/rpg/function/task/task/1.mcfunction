scoreboard players add @s task 1
execute as @s[scores={task=1}] at @s run playsound minecraft:block.beacon.power_select player @s
execute as @s[scores={task=1}] at @s run tellraw @s ["",{"text":"——————————————————————————\\n楔子","bold":true,"color":"#ff3300"},{"text":" 混乱的序章","bold":true},"\\n  那是一片充满哀嚎的土地。\\n  骸骨浸染大地，血色的玫瑰自尸骸边孕育，留下娇滴滴的血珠。铅色的天空被战火点燃，露出鎏金色的火焰，将远处的山峰融化，把残存的生灵屠戮殆尽。\\n  这是天使与恶魔的战争，他们将鲜血肆意涂抹，将枯骨化作利刃，刺入敌人的胸膛。惨烈已经不足以形容这场战争，这是神魔所主宰的领域，人类在这里只不过是卑贱的奴仆，匍匐在巨人的脚下，卖弄着自己的信仰。\\n  突然，有人拨开久不见晴的云层，撕开皲裂的天空，自高天而来，睥睨的目光死死盯着撒旦，那是天使的主宰-Michael。祂将胸膛撕裂，露出根根带血的肋骨，肆意抽出一根，滚烫的火焰开始在骨头上翻腾，高温将他融化，将他塑形，最终化作坚实的利刃，祓除不臣，涤荡天下。\\n  战争从来都是不死不休的，能停止它的，唯有死亡。\\n  持剑者瞬息间闪身至恶魔身前，伶俐的刀罡接踵而至，留下可怖的刀疤。血红色的蒸汽在刀口上腾起。可恶魔并没有闪退，伤口在几个呼吸间愈合，利爪贯穿胸膛，血液泵涌而出，顷刻涂满了祂的双手，如嗜血的猎犬，贪婪的审视自己的猎物。这便是恶魔的战争，肉体的搏杀不过是孩童的闹剧，唯有直击灵魂的伤害，才能逆转瞬息的局势。\\n  血液不断的溅射到地面，留下的，是渗入土地后残存的血痂。时间已在厮杀中流逝了许久，愈发浓郁的哀嚎声氤氲在这片糜烂的土地上，恶魔俨然落入下风，残缺的身躯已经跟不上恢复的速度，恶魔的君王在这一刻体会到了名为死亡的威胁，可魔鬼的高傲并不会让祂俯首系颈，这也注定了这场无休止的争斗仍会继续进行。\\n  持剑者猛地闪身至穹顶之上，撑起残缺的天空，裹挟着天上的雷光，化作泛着波澜的锁链，从天而降。锁链束缚了古龙的后颈，那古龙，自然是撒旦，也是曾经的拂晓之星-Lucifer。古龙是祂真正的躯体，代表至强至暴的权柄。可如今，却被雷光送入深不见底的极渊，天使把祂封入其中，让祂不能再度从地狱爬起，蛊惑世间的生灵。\\n  或许是劫后余生的喜悦，或许是千年的时光对比永无尽头的寿命不过浮海一粟，古龙在这一刻笑了起来，那是野兽般面容上露出的狰狞笑容，是嗜血猛兽的最后狂欢，祂缓缓的张口，为自己献上悼词：\\n\\n  “那一千年完了\\n  撒旦必从监牢里被释放\\n  出来要迷惑地上四方的列国\\n  就是歌革和玛各\\n  叫他们聚集争战\\n  他们的人数多如海沙”\\n  在最后一刻，祂的笑容依旧固定在脸上，仿佛胜券在握的赌徒，押上了所有的筹码，静待着千年后的胜利。\\n战火终于熄灭，骤雨倾盆，雨滴映出血红的倒影，露出悼亡者的面容。\\n  但无论如何，一切都结束了，一切也刚刚开始...\\n",{"text":"——————————————————————————","bold":true,"color":"#ff3300"}]
execute as @s[scores={task=1}] at @s run title @s title {"text":"\\ue101\\ue102\\ue103"}
execute as @s[scores={task=1}] at @s run title @s subtitle ["",{"text":"楔子","color":"#ff3300","bold":true}," 混乱的序章"]
execute as @s[scores={task=2}] at @s run title @s title ["",{"text":"任务目标","color":"white"},{"text":" 活下去!!!","color":"#ff3300","bold":true}]
execute as @s[scores={task=2}] at @s run title @s subtitle ["",{"text":"TASK OBJECTIVE ： TO ALIVE","bold":true}]
execute as @s[scores={task=2}] at @s run summon vindicator ~8 ~ ~6 {Johnny:1,Tags:["dev"],equipment:{head:{id:wither_skeleton_skull,components:{enchantments:{knockback:1}},count:1},mainhand:{id:netherite_sword,components:{custom_model_data:{floats:[1110008.0f]}},count:1}},drop_chances:{feet:0f,legs:0f,chest:0f,head:0f,mainhand:0f}}
execute as @s[scores={task=2}] at @s run summon vindicator ~-9 ~ ~7 {Johnny:1,Tags:["dev"],equipment:{head:{id:wither_skeleton_skull,components:{enchantments:{knockback:1}},count:1},mainhand:{id:netherite_sword,components:{custom_model_data:{floats:[1110008.0f]}},count:1}},drop_chances:{feet:0f,legs:0f,chest:0f,head:0f,mainhand:0f}}
execute as @s[scores={task=2}] at @s run summon vindicator ~-8 ~ ~-6 {Johnny:1,Tags:["dev"],equipment:{head:{id:wither_skeleton_skull,components:{enchantments:{knockback:1}},count:1},mainhand:{id:netherite_sword,components:{custom_model_data:{floats:[1110008.0f]}},count:1}},drop_chances:{feet:0f,legs:0f,chest:0f,head:0f,mainhand:0f}}
execute as @s[scores={task=2}] at @s run summon vindicator ~7 ~ ~-10 {Johnny:1,Tags:["dev"],equipment:{head:{id:wither_skeleton_skull,components:{enchantments:{knockback:1}},count:1},mainhand:{id:netherite_sword,components:{custom_model_data:{floats:[1110008.0f]}},count:1}},drop_chances:{feet:0f,legs:0f,chest:0f,head:0f,mainhand:0f}}
execute as @s[scores={task=2}] at @s run summon vindicator ~8 ~ ~-6 {Johnny:1,Tags:["dev"],equipment:{head:{id:wither_skeleton_skull,components:{enchantments:{knockback:1}},count:1},mainhand:{id:netherite_sword,components:{custom_model_data:{floats:[1110008.0f]}},count:1}},drop_chances:{feet:0f,legs:0f,chest:0f,head:0f,mainhand:0f}}
execute as @s[scores={task=2}] at @s run summon vindicator ~-9 ~ ~-7 {Johnny:1,Tags:["dev"],equipment:{head:{id:wither_skeleton_skull,components:{enchantments:{knockback:1}},count:1},mainhand:{id:netherite_sword,components:{custom_model_data:{floats:[1110008.0f]}},count:1}},drop_chances:{feet:0f,legs:0f,chest:0f,head:0f,mainhand:0f}}
execute as @s[scores={task=2}] at @s run summon vindicator ~8 ~ ~5 {Johnny:1,Tags:["dev"],equipment:{head:{id:wither_skeleton_skull,components:{enchantments:{knockback:1}},count:1},mainhand:{id:netherite_sword,components:{custom_model_data:{floats:[1110008.0f]}},count:1}},drop_chances:{feet:0f,legs:0f,chest:0f,head:0f,mainhand:0f}}
execute as @s[scores={task=2}] at @s run summon vindicator ~-5 ~ ~9 {Johnny:1,Tags:["dev"],equipment:{head:{id:wither_skeleton_skull,components:{enchantments:{knockback:1}},count:1},mainhand:{id:netherite_sword,components:{custom_model_data:{floats:[1110008.0f]}},count:1}},drop_chances:{feet:0f,legs:0f,chest:0f,head:0f,mainhand:0f}}
execute as @s[scores={task=3}] at @s at @e[type=minecraft:vindicator,tag=dev,distance=..6] run summon lightning_bolt
execute as @s[scores={task=3}] at @s at @e[type=minecraft:vindicator,tag=dev,distance=..6] run particle sculk_soul ~0.25 ~1.2 ~0.25 -0.5 -1 -0.5 0.1 50
execute as @s[scores={task=3}] at @s as @e[type=minecraft:vindicator,tag=dev,distance=..6] at @s run kill 
execute as @s[scores={task=3}] at @s run title @s title ["",{"text":"任务目标","color":"white"},{"text":" 弑神","color":"#ff3300","bold":true}]
execute as @s[scores={task=3}] at @s run title @s subtitle ["",{"text":"TASK OBJECTIVE ： KILLING GOD","bold":true}]








