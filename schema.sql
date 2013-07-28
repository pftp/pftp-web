drop table if exists exercises;
create table exercises (
  id integer primary key autoincrement,
  prompt text not null,
  hint text not null,
  test_cases text not null,
  solution text not null
);
