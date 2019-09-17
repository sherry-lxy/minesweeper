#include<stdio.h>
#include<stdlib.h> // rand関数を使用するために必要
#include<time.h> // time関数を使用するために必要

#define MS_SIZE 8 // ゲームボードのサイズ(変更不可)
#define MINE -1 // 地雷のセル
#define FLAG 2 // フラグを設置したセル
#define OPEN 1 // 開いたセル

int main(void)
{
    int mode; // モードを放置 (モード：セルを開く、フラグを立てる/除去する)
    int number_of_mines; // 地雷数のデフォルト値
    int mine_map[MS_SIZE][MS_SIZE]; // 地雷セルと数字セルを記録
    int game_board[MS_SIZE][MS_SIZE]; // ゲームの進行を記録するためのゲームボード

    int count; // 立ったフラグの数を数える

    int again=1,choose; // ゲームもう一回やるについての設置
    
    srand((unsigned)time(NULL)); // time関数で現在時刻を取得し、乱数を初期化する
    
    // 課題1 課題2    
    int x,y; // 2次元配列で使うために
    int n=0; // 地雷かどうかを判断するために
    int i,j; // 2次元配列で使うため

    printf("\n%d× %dのボードの各セルに配置された地雷を除去するゲームです。\n", MS_SIZE, MS_SIZE);
    printf("ゲームを始めます。\n");

    while(again==1){
        printf("\n地雷数を設定してください。(1~%d)： ",(MS_SIZE*MS_SIZE)-1);
        scanf("%d", &number_of_mines);
        while(number_of_mines==0 || number_of_mines>=MS_SIZE*MS_SIZE){
	    printf("地雷数が正しくありません\n");
	    printf("地雷数を設定してください。(1~%d)： ",(MS_SIZE*MS_SIZE)-1);
	    scanf("%d", &number_of_mines);
        }

	printf("\n");

        // 初期化
        for(y=0; y<MS_SIZE; y++){

	    for(x=0; x<MS_SIZE; x++){
	        mine_map[y][x]=0;
	    }
        }

        // 地雷の位置をrand関数で決める
        for(i=0; i<number_of_mines; i++){
 	    y=rand()%MS_SIZE;
	    x=rand()%MS_SIZE;
            while(mine_map[y][x]==MINE){ // もう設定した場合
	        y=rand()%MS_SIZE;
	        x=rand()%MS_SIZE;
	    }
	    mine_map[y][x]=MINE;
        }
	
        // 各セルの8近傍の地雷をカウント
        for(y=0;y<MS_SIZE;y++){
            for(x=0;x<MS_SIZE;x++){
	        if(mine_map[y][x]==MINE){ // セルは地雷かどうかを判断する
	        }
	        else{
		    for(j=-1;j<2;j++){
		        for(i=-1;i<2;i++){
			    if(y+j<0 || x+i<0 || y+j>7 || x+i>7){
			    }
			    else{
			        if(mine_map[y+j][x+i]==MINE){ // 8近傍のセルは地雷かどうかを判断する
			            mine_map[y][x] +=1;
				}
			    }
			}
		    }
		}
	    }
	}
      
        // 課題3
        int a,b; // セルを選択するために
        int win=0; // ゲームを続けるかどうかを判断するために

        // 初期化する
        for(y=0;y<MS_SIZE;y++){
	    for(x=0;x<MS_SIZE;x++){
	       game_board[y][x]=0;
	    }
	}

        // 全体を表示する
        printf("[y]\n\n");

        for(y=0;y<MS_SIZE;y++){
  	    printf("%2d|",y);		
	    for(x=0;x<MS_SIZE;x++){
                printf("  x");
	    }
	    printf("\n");
        }

        printf("   ");
        for(x=0;x<MS_SIZE;x++){
	    printf("---");
        }	
        printf("\n");
        printf("   ");
        for(x=0;x<MS_SIZE;x++){
	    printf("%3d",x);
        }
        printf("  [x]\n\n");

        while(win==0){ // ゲームを続ける条件
            printf("モードを選択してください：セルを開く(1)、フラグを設置/除去する：(2)：");
	    scanf("%d",&mode);

	    while(mode!=1 && mode!=2){
	       printf("1か2を入力してください：");
	       scanf("%d",&mode);
	    }
		
	    // ユーザがセルを指定		
	    if(mode==1){
	        printf("セルを開きます。\n");
	        printf("[x]と[y]を入力してください。\n");
	        printf("[x]:");
	        scanf("%d",&a);
	        printf("[y]:");
	        scanf("%d",&b);
	        printf("\n");

	        while(a<0 || a>7 || b<0 || b>7){ // セル内かどうかを判断する
	            printf("0から7までの整数を入力してください。\n");
		    printf("[x]:");
		    scanf("%d",&a);
		    printf("[y]:");
		    scanf("%d",&b);
		    printf("\n");
	        }

	        if(mine_map[b][a]==MINE){ //地雷を選択した場合
		    printf("GAME OVER!\n");
		    win=1;

	        }

	        else{
		    game_board[b][a]=OPEN;
	            // 選択したセルの8近傍のセルを設定する
	            for(j=-1;j<2;j++){
		        for(i=-1;i<2;i++){
                            if(b+j<0 || a+i<0 || b+j>7 || a+i>7){
			    }
			    else{
                                if(game_board[b+j][a+i]==FLAG){
                                    game_board[b+j][a+i]=FLAG;
			        }
			        else{
			            game_board[b+j][a+i]=OPEN;
			        }
			    } 
			}
		    }
		}
	    }

	    // 課題4
	    else{ // フラグを設置/除去する
	        printf("フラグを設置/除去します。\n");
                printf("[x]と[y]を入力してください。\n");
	        printf("[x]:");
	        scanf("%d",&a);
	        printf("[y]:");
	        scanf("%d",&b);

	        while(a<0 || a>7 || b<0 || b>7){ // セル内か判断
		    printf("0から7までの整数を入力してください。\n");
	            printf("[x]:");
	            scanf("%d",&a);
	            printf("[y]:");
	            scanf("%d",&b);
	        }

	        if(game_board[b][a]==FLAG){ // グラフもう設置した場合
		    game_board[b][a]=OPEN;
	        }
	        else{
	            game_board[b][a]=FLAG;
	        }
	    }

            // 全体を表示する
	    if(win==0){
                printf("[y]\n\n");

                for(y=0;y<MS_SIZE;y++){
                    printf("%2d|",y);		
	            for(x=0;x<MS_SIZE;x++){
		        // 選択したセルの8近傍のセルだけを表示する
		        if(game_board[y][x]==OPEN){
                            if(mine_map[y][x]==0){ // 選択したセルの8近傍のセルが0の場合は何も表示しない
			        printf("   "); 
		            }
			    else if(mine_map[y][x]==MINE){ // 地雷のセル
			        printf("  x");
			    }
		            else{
			        printf("%3d",mine_map[y][x]);
		            }
		        }
		        else if(game_board[y][x]==FLAG){ // フラグを設置したセル
			    printf("  F");
		        }
		        else{
		            printf("  x");
		        }
	             }
	             printf("\n");
                }
                printf("   ");
                for(x=0;x<MS_SIZE;x++){
	            printf("---");
                }	
                printf("\n");
                printf("   ");
                for(x=0;x<MS_SIZE;x++){
	            printf("%3d",x);
                }
                printf("  [x]\n\n");
	    }
	    // 課題５
	    count=0;

	    // 開いたセルを数える
  	    for(y=0;y<MS_SIZE;y++){
	        for(x=0;x<MS_SIZE;x++){
		    if(game_board[y][x]==OPEN){
        	        count +=1;
	            }
                }
	    }
		   		
	    if(count==((MS_SIZE*MS_SIZE)-number_of_mines)){ // ゲームクリアの条件
	        printf("Congratulation!\n");

		win=1;
	    }
        }

        // 結果
        printf("\n*************結果*************\n\n");

        printf("[y]\n\n");

        for(y=0;y<MS_SIZE;y++){
	    printf("%2d|",y);		
            for(x=0;x<MS_SIZE;x++){
	        if(mine_map[y][x]==MINE){
		    printf("  M");
	        }
		else if(mine_map[y][x]==0){
		    printf("   ");
		}
	        else{
	            printf("%3d",mine_map[y][x]);
	        }
	    }
	    printf("\n");
        }

        printf("   ");
        for(x=0;x<MS_SIZE;x++){
	    printf("---");
        }	
        printf("\n");
        printf("   ");
        for(x=0;x<MS_SIZE;x++){
	    printf("%3d",x);
        }
        printf("  [x]\n\n");

        printf("ここで、Mは地雷です。\n\n");

        printf("ゲームを続行しますか？(Yes:1 No:2)");
        scanf("%d",&choose);

        again=choose;
    }


    return 0;    
}
