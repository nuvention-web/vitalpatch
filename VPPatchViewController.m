//
//  VPPatchViewController.m
//  VitalPatch
//
//  Created by Sam Toizer on 1/27/14.
//  Copyright (c) 2014 Northwestern University. All rights reserved.
//

#import "VPPatchViewController.h"

@implementation VPPatchViewController

@synthesize patch = _patch;

- (id)initWithPatch:(VPPatch*)p {
    self = [super init];
    if (self) {
        self.patch = p;
        self.title = self.patch.name;
    }
    return self;
}

- (void)viewDidLoad {
    UILabel* label = [[UILabel alloc] initWithFrame:CGRectMake(10, 10, 200, 20)];
    label.text = self.patch.name;
    label.textColor = [UIColor blackColor];
    [self.view addSubview:label];
    
    UILabel* tempLabel = [[UILabel alloc] initWithFrame:CGRectMake(10, 30, 200, 20)];
    NSString* temp = @"Temperature: ";
    temp = [temp stringByAppendingFormat:@"%@", self.patch.temp];
    tempLabel.text = temp;
    tempLabel.textColor = [UIColor blackColor];
    [self.view addSubview:tempLabel];
    
    UILabel* pulseLabel = [[UILabel alloc] initWithFrame:CGRectMake(10, 50, 200, 20)];
    NSString* pulse = @"Pulse: ";
    pulse = [pulse stringByAppendingFormat:@"%@", self.patch.pulse];
    pulseLabel.text = pulse;
    pulseLabel.textColor = [UIColor blackColor];
    [self.view addSubview:pulseLabel];
    
//    UIButton* searchButton = [UIButton buttonWithType:UIButtonTypeRoundedRect];
//    searchButton.frame = CGRectMake(5, 5, 30, 30);
//    searchButton.titleLabel.text = @"Search";
//    searchButton.backgroundColor = [UIColor whiteColor];
//    [searchButton addTarget:self action:@selector(showCityFinder:) forControlEvents:UIControlEventTouchUpInside];
//    [self.view addSubview:searchButton];
}



@end
