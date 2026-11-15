# summon 第 36 刻的姿势（每 1 刻一帧，补间 1 刻）。由 add_leviathan_model.py 烘焙。
execute on passengers if entity @s[tag=rpg.lv.p.l_leg] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.15157f,-1.63555f,-0.05346f],left_rotation:[0.70626f,0.03446f,0.03446f,0.70627f],scale:[7.5497f,7.5497f,7.5497f],right_rotation:[0f,0f,0f,1f]}}
execute at @s run playsound rpg:leviathan.summoned hostile @a[distance=..24] ~ ~ ~ 1 0.8
