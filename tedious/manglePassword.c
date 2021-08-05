undefined8 main(void) {
  // initializations
  long lVar1;
  undefined8 *puVar2;
  long in_FS_OFFSET;
  //byte bVar3;
  int i;
  undefined8 local_d8;
  int local_d0;
  int local_cc;
  int local_c8;
  int local_c4;
  int local_c0;
  int local_bc;
  int local_b8;
  int local_b4;
  int local_b0;
  int local_ac;
  int local_a8;
  int local_a4;
  int local_a0;
  int local_9c;
  int local_98;
  int local_94;
  int local_90;
  int local_8c;
  int local_88;
  int local_84;
  int local_80;
  int local_7c;
  int local_78;
  int local_74;
  int local_70;
  int local_6c;
  int local_68;
  int local_64;
  int local_60;
  int local_5c;
  int local_58;
  int local_54;
  int local_50;
  int local_4c;
  int local_48;
  int local_44;
  int local_40;
  char input [40];
  long local_10;
  //bVar3 = 0;
  local_10 = *(long *)(in_FS_OFFSET + 40);

  // asks for the flag and puts it into input
  puts("Enter the flag:");
  fgets((char *)input,40,stdin);

  /*
  for (int i = 0; i < 39; i++) {
    input[i] += 0x3b ^ 0x38;//3
  }

  for (int i = 0; i < 39; i++) {
    input[i] += 0x12 ^ 0xfd;//239
  }

  for (int i = 0; i < 39; i++) {
    input[i] += 4 ^ 0x50;//84
  }

  for (int i = 0; i < 39; i++) {
    input[i] += 0x13 ^ 0x68;//123
  }

  for (int i = 0; i < 39; i++) {
    input[i] += 0xc ^ 0x79;//117
  }

  for (int i = 0; i < 39; i++) {
    input[i] += 0xbc ^ 0xa0;//28
  }

  for (int i = 0; i < 39; i++) {
    input[i] += 10 ^ 0xcd;//199
  }

  for (int i = 0; i < 39; i++) {
    input[i] += 0xb8 ^ 0x5a;//226
  }

  for (int i = 0; i < 39; i++) {
    input[i] += 0xb ^ 0xbd;//182
  }

  for (int i = 0; i < 39; i++) {
    input[i] -= 0x1f ^ 0xed;//242
  }

  for (int i = 0; i < 39; i++) {
    input[i] += 0x45 ^ 0x22;//103
  }

  for (int i = 0; i < 39; i++) {
    input[i] += 0xbe ^ 0x6b;//213
  }

  for (int i = 0; i < 39; i++) {
    input[i] -= 38 ^ 0x6b;//77
  }

  for (int i = 0; i < 39; i++) {
    input[i] += 0x76 ^ 0xfa;//140
  }

  for (int i = 0; i < 39; i++) {
    input[i] += 0x16 ^ 0x6b;//125
  }

  for (int i = 0; i < 39; i++) {
    input[i] += 0xb5 ^ 0x6b;//222
  }

  for (int i = 0; i < 39; i++) {
    input[i] += 0x8d ^ 100;//233
  }

  for (int i = 0; i < 39; i++) {
    input[i] += 10 ^ 0xab;//161
  }

  for (int i = 0; i < 39; i++) {
    input[i] += 99 ^ 0x1b;//120
  }

  for (int i = 0; i < 39; i++) {
    input[i] -= 0x2b ^ 0xf0;//219
  }

  for (int i = 0; i < 39; i++) {
    input[i] += 0x75 ^ 0x6b;//30
  }
  input[39] = 0;
  */

  // adds 2010 to each number
  for (int i = 0; i < 38; i++) {
    input[i] += 2010;
  }

  // clears everything?
  puVar2 = &local_d8;
  for (int j = 20; j != 0; j--) {
    *puVar2 = 0;
    puVar2++;// = puVar2 + 1;//(bVar3 * -2) + 1;
  }

  local_d8._0_4_ = 0x4d;
  local_d8._4_4_ = 0xb9;
  local_d0 = 0x4d;
  local_cc = 0xb;
  local_c8 = 0xd4;
  local_c4 = 0x66;
  local_c0 = 0xe3;
  local_bc = 0x29;
  local_b8 = 0xb8;
  local_b4 = 0x4d;
  local_b0 = 0xdf;
  local_ac = 0x66;
  local_a8 = 0xb8;
  local_a4 = 0x4d;
  local_a0 = 0xe;
  local_9c = 0xc4;
  local_98 = 0xdf;
  local_94 = 0xd4;
  local_90 = 20;
  local_8c = 0x3b;
  local_88 = 0xdf;
  local_84 = 0x66;
  local_80 = 0x2c;
  local_7c = 20;
  local_78 = 0x47;
  local_74 = 0xdf;
  local_70 = 0xb7;
  local_6c = 0xb8;
  local_68 = 0xb7;
  local_64 = 0xdf;
  local_60 = 0x47;
  local_5c = 0x4d;
  local_58 = 0xa4;
  local_54 = 0xdf;
  local_50 = 0x32;
  local_4c = 0xb8;
  local_48 = 0xea;
  local_44 = 0xf5;
  local_40 = 0x92;
  i = 0;

  for (int i = 0; i <= 38; i++) {
    if (i==38) {
      printf("GOOD JOB!");
    }
    else if (input[i] != local_d8 + (i*4)) {
      printf("WRONG!! ");
      break;
    }
  }
  return 0;
}
