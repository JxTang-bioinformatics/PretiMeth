/***********************************************************
File name: pierson.cpp
Author: Tang Jianxiong
Description: main
Date: 2018/11/10
Remarks：Calculate the pearson correlation coefficient
***********************************************************/
// pearson.cpp: Define the entry point for the console application.
//

#include "pch.h"
#include<iostream>
#include<vector>
#include<time.h>
#include<ctime>
#include<fstream>
#include<string>

#define EXPLEN 413719// Number of model loci
#define OBSLEN 450137// Number of feature loci
#define TESTLOCK 413719//  Non-test condition set to EXPLEN
#define DIMS 665// Number of samples

using namespace std;
int main() {

	/*Data file name*/
	char expfn[] = "expfileforDemo100_665.txt";
	char obsfn[] = "obsfileforDemo10000_665.txt";

	double start, stop;
	fstream f(expfn);
	fstream fobs(obsfn);
	string line;
	int i = 1;

	/*Load exp*/
	double** exps = new double*[EXPLEN];
	int expidx = 0;
	while (getline(f, line))
	{
		double* exp = new double[DIMS]();
		int idx = 11; int numidx = 0;
		string value = "";
		while (line[idx] != NULL) {

			if (line[idx] != ' ' && line[idx] != '\t') {
				value += line[idx];

			}
			else {
				if (value != "") {
					exp[numidx] = stod(value);
				}
				value = "";
				numidx++;
			}
			idx++;
		}
		if (value!= ""){exp[numidx] = stod(value);}
		



		exps[expidx] = exp;
		expidx++;
		if (expidx == EXPLEN) { break; }

	}
	cout << "exp file finished" << endl;

	/*Load obs*/
	double** obss = new double*[OBSLEN];
	int obsidx = 0;
	while (getline(fobs, line))
	{
		double* obs = new double[DIMS]();
		int idx = 11; int numidx = 0;
		string value = "";
		while (line[idx] != NULL) {

			if (line[idx] != ' ' && line[idx] != '\t') {
				value += line[idx];

			}
			else {
				if (value != "") {
					obs[numidx] = stod(value);
				}
				value = "";
				numidx++;
			}
			idx++;
		}
		if (value != "") { obs[numidx] = stod(value); }
		


		obss[obsidx] = obs;
		obsidx++;
		//if (obsidx == 100) {
		//	break;
		//}
	}
	cout << "obs file finished" << endl;


	start = clock();
	auto ptrexp = exps;
	ofstream fout("meth_peason_noabs_672_10_0522.txt");
	/*main loop*/
	for (int m = 0; m < TESTLOCK; m++) {
		auto ptr = obss;
		double* corrs = new double[OBSLEN]();

		for (int k = 0; k < OBSLEN; k++) {

			double sum_bb = 0.0;
			double sum_ab = 0.0;
			double corr = 0.0;
			double sum_a = 0.0;
			double sum_b = 0.0;
			double sum_aa = 0.0;
			int lengh = DIMS;
			double a = 0.0;
			double b = 0.0;
			for (i = 0; i < DIMS; i++)
			{
				a = *(*(ptrexp)+i);
				b = *(*(ptr)+i);
				if (a == 0 || b == 0) {
					lengh -= 1;
				}
				else
				{
					sum_a += a;
					sum_b += b;
					sum_aa += a * a;
					sum_ab += a * b;
					sum_bb += b * b;
				}
			}
			ptr++;
			corr = (sum_aa - sum_a * sum_a / lengh) * (sum_bb - sum_b * sum_b / lengh);
			corr = corr > 0 ? (sum_ab - sum_a * sum_b / lengh) / sqrt(corr) : 0;
			
			corrs[k] = corr;
		}

		/*seek for biggest ten*/
		//vector<int> bigTenidx(0);//索引
		//vector<double> bigTenvla(0);//值
		for (int maxcnt = 0; maxcnt < 10; maxcnt++) {
			auto pbig = corrs + maxcnt;
			auto corridx = corrs + maxcnt;
			int tenidx = 0;
			int residx = 0;
			while (*(corridx))
			{
				if (abs(*pbig) <= abs(*corridx)) {
					pbig = corridx;
					residx = tenidx;
				}
				corridx++;
				tenidx++;
			}
			fout << residx << ' ' << *pbig << '\t';
			auto tmp = *(corrs + maxcnt);
			*(corrs + maxcnt) = *pbig;
			*pbig = tmp;
			/*bigTenidx.push_back(residx);*/
		}
		//for (auto it : bigTenvla) {
		//	fout << it << '\t';
		//}
		//fout << endl;
		//for (auto it : bigTenidx) {
		//	fout << it << '\t';
		//}
		fout << endl;
		delete[]corrs;
		ptrexp++;

		if (m % 10000 == 0) {
			cout << m << endl;
		}

	}
	fout.close();


	stop = clock();
	cout << "time is: "
		<< stop - start
		<< "ms"
		<< endl;
	getchar();

	return 0;
}
