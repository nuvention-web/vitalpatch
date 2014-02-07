//
//  VPPatchViewController.h
//  VitalPatch
//
//  Created by Sam Toizer on 1/27/14.
//  Copyright (c) 2014 Northwestern University. All rights reserved.
//

#import <UIKit/UIKit.h>
#import "VPPatch.h"

@interface VPPatchViewController : UIViewController

@property (strong, nonatomic) VPPatch* patch;

- (id)initWithPatch:(VPPatch*)p;

@end
