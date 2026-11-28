$execute as @e[tag=rpg.unit.f,distance=$(lo)..$(hi),tag=!rpg.mkb.sw$(id)] if predicate rpg:michael_boss_i1/grounded run function rpg:michael_boss_i1/sanctus/burn {id:$(id)}
